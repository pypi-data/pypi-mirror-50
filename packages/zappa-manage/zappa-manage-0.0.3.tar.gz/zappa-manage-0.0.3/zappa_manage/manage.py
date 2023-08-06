#!/usr/bin/python

import boto3
import click
from pybase64 import b64encode

from asym_crypto_yaml import (
    load, Encrypted, decrypt_value,
    load_private_key_from_file,
    load_private_key_from_string
)


def perform_deploy_lambda_envs(config_file_path, private_key_content, private_key_path, kms_key_arn, lambda_name):
    """
    Loads private key to deploy the application's secret values to corresponding lambda
    :config_file_path = path to config file
    :private_key_content = content of private key
    :private_key_path = path to the private key
    :kms_key_arn = arn for an aws kms_key
    :lambda_name = name of an aws lambda function
    """
    private_key = None
    if private_key_path is not None:
        private_key = load_private_key_from_file(private_key_path)

    elif private_key_content is not None:
        # GoCD will mangle the encrypted key when it is passed in this way
        # The following lines unmangle the key.
        private_key_content = private_key_content.replace(' ', '\n')
        private_key_content = private_key_content.replace('-----BEGIN\nRSA\nPRIVATE\nKEY-----', '-----BEGIN RSA PRIVATE KEY-----')
        private_key_content = private_key_content.replace('-----END\nRSA\nPRIVATE\nKEY-----', '-----END RSA PRIVATE KEY-----')
        private_key = load_private_key_from_string(private_key_content.encode('utf-8'))

    if private_key is None:
        raise ValueError('You must specify the private key either by PRIVATE_KEY ENV, or with private-key-path')

    push_config_and_secrets_to_lambda_env(config_file_path, private_key, kms_key_arn, lambda_name)


def push_config_and_secrets_to_lambda_env(config_file_path, private_key, kms_key_arn, lambda_name):
    """
    Pushes the application's configurations and secret (encrypted) values to
    the corresponding lambda function. The application will have to decrypt value
    :config_file_path = path to config file
    :private_key = private key of application
    :kms_key_arn = arn for an aws kms_key
    :lambda_name = name of an aws lambda function
    """
    with open(config_file_path, "r") as f:
        config = load(f)
    if (config is None):
        config = {}

    for key,value in config.items():
        if (type(value) == Encrypted):
            config[key] = kms_encrypt(kms_key_arn, decrypt_value(value, private_key))

    client = boto3.client('lambda')
    response = client.update_function_configuration(
        FunctionName=lambda_name,
        Environment={
            'Variables': config
        }
    )

def kms_encrypt(kms_key_arn, value):
    """
    Uses AWS KMS to encrypt the value of an environment variable
    :kms_key_arn = arn for an aws kms_key
    :value = the value of an environment variable
    """
    client = boto3.client('kms')

    response = client.encrypt(
       KeyId=kms_key_arn,
       Plaintext=value,
    )

    # returns the encrypted 64 bit string
    return b64encode(response[u'CiphertextBlob']).decode()
