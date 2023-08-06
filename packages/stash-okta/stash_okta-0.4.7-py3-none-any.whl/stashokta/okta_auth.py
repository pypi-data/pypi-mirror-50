""" Handles auth to Okta and returns SAML assertion """
# pylint: disable=C0325,R0912,C1801
import sys
import os
import time
from configparser import RawConfigParser
from getpass import getpass
from bs4 import BeautifulSoup as bs
import requests


class OktaAuth(object):
    # pylint: disable=too-many-instance-attributes
    """ Handles auth to Okta and returns SAML assertion """
    def __init__(self, okta_profile, verbose, logger, totp_token):
        home_dir = os.path.expanduser('~')
        okta_config = home_dir + '/.okta-aws'
        parser = RawConfigParser()
        parser.read(okta_config)
        profile = okta_profile
        self.totp_token = totp_token
        self.logger = logger
        self.factor = ""
        self.duration = self.default_duration_seconds
        if parser.has_option(profile, 'base-url'):
            self.base_url = "https://%s" % parser.get(profile, 'base-url')
            self.logger.info("Authenticating to: %s" % self.base_url)
        else:
            self.logger.error("No base-url set in ~/.okta-aws")
            exit(1)
        if parser.has_option(profile, 'username'):
            self.username = parser.get(profile, 'username')
            self.logger.info("Authenticating as: %s" % self.username)
        else:
            self.username = input('Enter username: ')  # nosec
        if parser.has_option(profile, 'password'):
            self.password = parser.get(profile, 'password')
        else:
            self.password = getpass('Enter password: ')

        if parser.has_option(profile, 'factor'):
            self.factor = parser.get(profile, 'factor')
            self.logger.debug("Setting MFA factor to %s" % self.factor)

        if parser.has_option(profile, 'duration'):
            self.duration = parser.get(profile, 'duration')
            self.logger.info("Setting duration in seconds to %s" % self.duration)

        self.verbose = verbose

    @property
    def default_duration_seconds(self):
        """Defines a default duration for which the creds are valid"""
        return 43200

    def get_duration(self):
        """Tries to retrieve a user configured duration"""
        try:
            return int(self.duration)
        except (ValueError, TypeError):
            return self.default_duration_seconds

    def primary_auth(self):
        """ Performs primary auth against Okta """

        auth_data = {
            "username": self.username,
            "password": self.password
        }
        resp = requests.post(self.base_url + '/api/v1/authn', json=auth_data)
        resp_json = resp.json()
        if 'status' in resp_json:
            if resp_json['status'] == 'MFA_REQUIRED':
                factors_list = resp_json['_embedded']['factors']
                state_token = resp_json['stateToken']
                session_token = self.verify_mfa(factors_list, state_token)
            elif resp_json['status'] == 'SUCCESS':
                session_token = resp_json['sessionToken']
        elif resp.status_code != 200:
            self.logger.error(resp_json['errorSummary'])
            exit(1)
        else:
            self.logger.error(resp_json)
            exit(1)

        return session_token

    def verify_mfa(self, factors_list, state_token):
        """ Performs MFA auth against Okta """

        possible_factor_types = ["token:software:totp", "push"]
        supported = []
        for factor in factors_list:
            if factor['factorType'] in possible_factor_types:
                supported.append(factor)
            else:
                self.logger.info("Unsupported factorType: %s" %
                                 (factor['factorType'],))

        supported = sorted(supported, key=lambda x: (x['provider'], x['factorType']))

        if len(supported) == 1:
            session_token = self.verify_single_factor(supported[0], state_token)
        elif len(supported) > 1:
            if not self.factor:
                print("Registered MFA factors:")
            for index, factor in enumerate(supported):
                factor_type = factor['factorType']
                provider = factor['provider']

                if provider == "GOOGLE":
                    name = "Google Authenticator"
                elif provider == "OKTA":
                    if factor_type == "push":
                        name = "Okta Verify - Push"
                    else:
                        name = "Okta Verify"
                else:
                    name = "Unsupported factor type: %s" % provider

                if self.factor:
                    if self.factor == provider:
                        choice = index
                        self.logger.info("Using pre-selected factor choice \
                                         from ~/.okta-aws")
                        break
                else:
                    print("%d: %s" % (index + 1, name))

            if not self.factor:
                choice = int(input('Please select the MFA factor: '))  # nosec

            self.logger.info("Performing secondary authentication using: %s | %s" %
                             (supported[choice - 1]['provider'],
                              supported[choice - 1]['factorType']))
            session_token = self.verify_single_factor(supported[choice - 1],
                                                      state_token)
        else:
            print("MFA required, but no supported factors enrolled! Exiting.")
            exit(1)

        return session_token

    def verify_single_factor(self, factor, state_token):
        """ Verifies a single MFA factor """
        req_data = {
            "stateToken": state_token
        }

        self.logger.debug(factor)

        if factor['factorType'] == 'token:software:totp':
            if self.totp_token:
                self.logger.debug("Using TOTP token from command line arg")
                req_data['answer'] = self.totp_token
            else:
                req_data['answer'] = input('Enter MFA token: ')  # nosec
        post_url = factor['_links']['verify']['href']
        resp = requests.post(post_url, json=req_data)
        resp_json = resp.json()
        if 'status' in resp_json:
            if resp_json['status'] == "SUCCESS":
                return resp_json['sessionToken']
            elif resp_json['status'] == "MFA_CHALLENGE":
                print("Waiting for push verification...")
                while True:
                    resp = requests.post(
                        resp_json['_links']['next']['href'], json=req_data)
                    resp_json = resp.json()
                    if resp_json['status'] == 'SUCCESS':
                        return resp_json['sessionToken']
                    elif resp_json['factorResult'] == 'TIMEOUT':
                        print("Verification timed out")
                        exit(1)
                    elif resp_json['factorResult'] == 'REJECTED':
                        print("Verification was rejected")
                        exit(1)
                    else:
                        time.sleep(0.5)
        elif resp.status_code != 200:
            self.logger.error(resp_json['errorSummary'])
            exit(1)
        else:
            self.logger.error(resp_json)
            exit(1)
        return None

    def get_session(self, session_token):
        """ Gets a session cookie from a session token """
        data = {"sessionToken": session_token}
        resp = requests.post(
            self.base_url + '/api/v1/sessions', json=data).json()
        return resp['id']

    def get_apps(self, session_id):
        """ Gets apps for the user """
        sid = "sid=%s" % session_id
        headers = {'Cookie': sid}
        resp = requests.get(
            self.base_url + '/api/v1/users/me/appLinks',
            headers=headers).json()
        aws_apps = []
        for app in resp:
            if app['appName'] == "amazon_aws":
                aws_apps.append(app)
        if not aws_apps:
            self.logger.error("No AWS apps are available for your user. \
                Exiting.")
            sys.exit(1)

        aws_apps = sorted(aws_apps, key=lambda a: a['sortOrder'])

        if len(aws_apps) == 1:
            label = aws_apps[0]['label']
            link_url = aws_apps[0]['linkUrl']
            print("Using AWS App: '%s'\nurl: '%s'" % (label, link_url))
            return label, link_url
        else:
            print("Available apps:")
            for index, app in enumerate(aws_apps):
                app_name = app['label']
                print("%d: %s" % (index + 1, app_name))

            app_choice = int(input('Please select AWS app: ')) - 1  # nosec

        return aws_apps[app_choice]['label'], aws_apps[app_choice]['linkUrl']

    def get_saml_assertion(self, html):
        """ Returns the SAML assertion from HTML """
        soup = bs(html.text, "html.parser")
        assertion = ''

        for input_tag in soup.find_all('input'):
            if input_tag.get('name') == 'SAMLResponse':
                assertion = input_tag.get('value')

        if not assertion:
            self.logger.error("SAML assertion not valid: " + assertion)
            exit(-1)
        return assertion

    def get_assertion(self):
        """ Main method to get SAML assertion from Okta """
        session_token = self.primary_auth()
        session_id = self.get_session(session_token)
        _, app_link = self.get_apps(session_id)
        sid = "sid=%s" % session_id
        headers = {'Cookie': sid}
        resp = requests.get(app_link, headers=headers)
        assertion = self.get_saml_assertion(resp)
        return assertion
