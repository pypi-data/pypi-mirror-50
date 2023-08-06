""" Wrapper script for awscli which handles Okta auth """
import logging
# pylint: disable=C0325,R0913,R0914
import os
from subprocess import check_output

import click
import yaml

from stashokta.aws_auth import AwsAuth
from stashokta.okta_auth import OktaAuth
from stashokta.version import __version__


def get_credentials(aws_auth, okta_profile,
                    verbose, logger, totp_token, duration):
    """ Gets credentials from Okta """

    okta = OktaAuth(okta_profile, verbose, logger, totp_token)
    assertion = okta.get_assertion()
    role = aws_auth.choose_aws_role(assertion)
    principal_arn, role_arn = role
    duration_seconds = okta.get_duration() if not duration else int(duration)

    sts_token = aws_auth.get_sts_token(
        role_arn, principal_arn, assertion, duration_seconds)
    access_key_id = sts_token['AccessKeyId']
    secret_access_key = sts_token['SecretAccessKey']
    session_token = sts_token['SessionToken']

    return {
        'access_key_id': access_key_id,
        'secret_access_key': secret_access_key,
        'session_token': session_token
    }


def use_credentials(aws_auth, profile, cache, verbose, credentials):
    """ Gets credentials from Okta """

    if not profile:
        exports = console_output(credentials['access_key_id'], credentials['secret_access_key'],
                                 credentials['session_token'], verbose)
        if cache:
            cache = open("%s/.okta-credentials.cache" %
                         (os.path.expanduser('~'),), 'w')
            cache.write(exports)
            cache.close()
        exit(0)
    else:
        aws_auth.write_sts_token(profile, credentials['access_key_id'],
                                 credentials['secret_access_key'], credentials['session_token'])


def ecs_cli_output(credentials):
    """Gets cli output from AWS ECS Service and exports to creds file"""

    home_dir = os.path.expanduser('~')
    credentials_path = os.path.join(home_dir, '.ecs', 'credentials')

    with open(credentials_path) as file:
        ecs_credentials_file = yaml.safe_load(file)

    profiles = ecs_credentials_file['ecs_profiles']

    if 'default' in profiles:
        default = profiles['default']
        default['aws_access_key_id'] = credentials['access_key_id']
        default['aws_secret_access_key'] = credentials['secret_access_key']
        default['aws_session_token'] = credentials['session_token']

    with open(credentials_path, "w") as file:
        yaml.dump(ecs_credentials_file, file, default_flow_style=False)


def console_output(access_key_id, secret_access_key, session_token, verbose):
    """ Outputs STS credentials to console """
    if verbose:
        print("Use these to set your environment variables:")
    exports = "\n".join([
        "export AWS_ACCESS_KEY_ID=%s" % access_key_id,
        "export AWS_SECRET_ACCESS_KEY=%s" % secret_access_key,
        "export AWS_SESSION_TOKEN=%s" % session_token
    ])
    print(exports)

    return exports


# pylint: disable=R0913
@click.command()
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose mode')
@click.option('-V', '--version', is_flag=True,
              help='Outputs version number and exits')
@click.option('-d', '--debug', is_flag=True, help='Enables debug mode')
@click.option('-f', '--force', is_flag=True, help='Forces new STS credentials. \
Skips STS credentials validation.')
@click.option('--okta-profile', help="Name of the profile to use in .okta-aws. \
If none is provided, then the default profile will be used.\n")
@click.option('--profile', help="Name of the profile to store temporary \
credentials in ~/.aws/credentials. If profile doesn't exist, it will be \
created. If omitted, credentials will output to console.\n")
@click.option('--ecs-profile', is_flag=True, help='update ~/.ecs/credentials.')
@click.option('-c', '--cache', is_flag=True, help='Cache the default profile credentials \
to ~/.okta-credentials.cache\n')
@click.option('--duration', help="number of seconds for token to be valid, max is 43200 (12 Hours)")
@click.option('-t', '--token', help='TOTP token from your authenticator app')
@click.option('-e', '--export_env', is_flag=True,
              help="Exports AWS environment variables to .env file. Default file path: ~/.aws/.env)"
                   "Use the --env_file option to specify a different file path.")
@click.option('--env_file', help="Name of .env file where AWS vars will be exported."
                                 "The -e option is not required if passing in --env_file.")
@click.argument('awscli_args', nargs=-1, type=click.UNPROCESSED)
def main(okta_profile, profile, verbose, version, ecs_profile,
         debug, force, cache, awscli_args, token, duration,
         export_env, env_file):
    """ Authenticate to awscli using Okta """

    if version:
        print(__version__)
        exit(0)
    # Set up logging
    logger = logging.getLogger('okta-awscli')
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(logging.WARN)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    if verbose:
        handler.setLevel(logging.INFO)
    if debug:
        handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    if not okta_profile:
        okta_profile = "default"
    aws_auth = AwsAuth(profile, okta_profile, verbose, logger)
    if not aws_auth.check_sts_token(profile) or force:
        if force and profile:
            logger.info("Force option selected, \
                getting new credentials anyway.")
        elif force:
            logger.info("Force option selected, but no profile provided. \
                Option has no effect.")
        credentials = get_credentials(aws_auth, okta_profile, verbose, logger, token, duration)

        use_credentials(aws_auth, profile, cache, verbose, credentials)

        if ecs_profile:
            ecs_cli_output(credentials)

        if env_file:
            aws_auth.export_env_vars(
                credentials['access_key_id'],
                credentials['secret_access_key'],
                credentials['session_token'],
                env_file_path=env_file
            )
        elif export_env:
            aws_auth.export_env_vars(
                credentials['access_key_id'],
                credentials['secret_access_key'],
                credentials['session_token']
            )

    if awscli_args:
        cmdline = ['aws', '--profile', profile] + list(awscli_args)
        logger.info('Invoking: %s', ' '.join(cmdline))
        check_output(cmdline, shell=False)  # nosec


if __name__ == "__main__":
    # pylint: disable=E1120
    main()
    # pylint: enable=E1120
