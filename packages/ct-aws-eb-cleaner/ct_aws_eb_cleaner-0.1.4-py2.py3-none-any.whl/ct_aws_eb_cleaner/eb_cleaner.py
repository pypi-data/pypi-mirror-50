# -*- coding: utf-8 -*-

"""
Main module.
This script aims to clear all applications versions from an ElasticBeanstalk environment that are not implemented. It assumes that aws client is installed and configured to run.
The procedures uses the aws terminal client, that is documented in the link: https://docs.aws.amazon.com/cli/latest/reference/elasticbeanstalk/index.html
"""
import json
import subprocess

from argparse import ArgumentParser, Namespace
from typing import Any


def get_args() -> Namespace:
    """
    Method to retrieve arguments from the command line.
    :return: argparse.Namespace
    """
    arg_parser = ArgumentParser(
        description='Script to clear all applications versions from an ElasticBeanstalk environment that are not '
                    'implemented.'
    )

    arg_parser.add_argument('--application-name', type=str, required=True, help='Application\'s environment name')

    return arg_parser.parse_args()


def execute(command: str) -> Any:
    """
    Method to execute a command in OS shell.
    :param command: command to be executed
    :return: command's response
    :raise Exception: if any error happens during the command's execution
    """
    out = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()
    if stderr is not None:
        raise Exception('[error] Trying to execute \'{}\'.\n[error] {}'.format(command, str(stderr)))
    else:
        return stdout


def eb_describe_environments(application_name: str) -> dict:
    """
    Method to retrieve all the environments details with the deployed applications versions.
    :param application_name:
    :return: dict
    """
    command = f"aws elasticbeanstalk describe-environments --application-name \"{application_name}\""
    command_response = execute(command)
    return json.loads(command_response)


def eb_describe_application_versions(application_name: str) -> dict:
    """
    Method to retrieve all the environment's applications versions.
    :param application_name:
    :return: dict
    """
    command = f"aws elasticbeanstalk describe-application-versions --application-name \"{application_name}\""
    command_response = execute(command)
    return json.loads(command_response)


def eb_delete_application_version(application_name: str, version_label: str):
    command = f"delete-application-version --application-name \"{application_name}\" --version-label \"{version_label}\""
    execute(command)


def run():
    args = get_args()

    print(f'[info] Retrieving deployed environments at: {args.application_name}...')
    environments = eb_describe_environments(application_name=args.application_name)

    print(f'[info] Retrieving environment\'s applications versions...')
    applications_versions = eb_describe_application_versions(application_name=args.application_name)

    print(f'[info] Identifying active environment\'s applications versions...')
    active_application_version = list()
    for env in environments['Environments']:
        active_application_version.append(env['VersionLabel'])

    print(f'[info] Deleting inactive environment\'s applications versions...')
    for app_version in applications_versions['ApplicationVersions']:
        if app_version['VersionLabel'] not in active_application_version:
            print('[info] Deleting application version \'{}\' in \'{}\' application environment.'.format(app_version['VersionLabel'], app_version['ApplicationName']))

    print(f'[info] Done.')
