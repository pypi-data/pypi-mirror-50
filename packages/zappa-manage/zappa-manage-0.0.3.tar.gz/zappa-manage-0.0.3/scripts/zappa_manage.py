import boto3
import click
from pybase64 import b64encode

from asym_crypto_yaml import (
    load, Encrypted, decrypt_value,
    load_private_key_from_file,
    load_private_key_from_string
)

from zappa_manage import perform_deploy_lambda_envs


@click.group()
def cli():
    pass

@click.command()
@click.option('--config_file_path', help='', required=True)
@click.option('--private_key_content', envvar='PRIVATE_KEY', help='')
@click.option('--private_key_path', help='')
@click.option('--kms_key_arn', help='', required=True)
@click.option('--lambda_name', help='', required=True)
def deploy_lambda_envs(config_file_path, private_key_content, private_key_path, kms_key_arn, lambda_name):
    """
    Loads private key to deploy the application's secret values to corresponding lambda
    :config_file_path = path to config file
    :private_key_content = content of private key
    :private_key_path = path to the private key
    :kms_key_arn = arn for an aws kms_key
    :lambda_name = name of an aws lambda function
    """
    perform_deploy_lambda_envs(config_file_path, private_key_content, private_key_path, kms_key_arn, lambda_name)


cli.add_command(deploy_lambda_envs)

if __name__ == '__main__':
    """Initializes the cli"""
    cli()
