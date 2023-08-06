#!/usr/bin/env python

# Copyright (c) 2019 Sarath Kumar Sivan, https://github.com/sarathkumarsivan
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import argparse
import base64
import os
import logging
import errno
import urllib3
import sys

from github import Github
from github import GithubException
from configurer import configure_logging_console

# Logger instance for pygithubctl.
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logger = configure_logging_console(logging.getLogger('pygithubctl'), format)


def download_file(repository, sha, source, target):
    """
    Downloads a single source file from the Git repository hosted on remote
    GitHub server to your local file system.

    :param repository: Git repository hosted on GitHub server
    :param sha: unique ID (a.k.a. the "SHA" or "hash") against the commit
    :param source: Path of resources on Git repository hosted on GitHub server.
    :param target: Path of target file on the local filesystem or disk.
    :returns: None
    :raises: GithubException: If there is any failure during download.
    """
    logger.info('Fetching %s from %s', source, repository)
    try:
        contents = repository.get_contents(source, ref=sha)
        data = base64.b64decode(contents.content)
        output = open(target, "w")
        output.write(data)
        output.close()
    except (GithubException, IOError) as exception:
        logger.error('Error downloading %s: %s', source, exception)
        raise GithubException("Failed to download the resource %s", source)


def download_directory(repository, sha, source, target):
    """
    Downloads the files and directories recursively from Git hosted on remote
    GitHub server to the local file system.

    :param repository: Git repository hosted on GitHub server
    :param sha: unique ID (a.k.a. the "SHA" or "hash") against the commit
    :param source: Path of resources on Git repository hosted on GitHub server.
    :param target: Path of target file on the local filesystem or disk.
    :returns: None
    :raises: GithubException: If there is any failure during download.
    """
    try:
        contents = repository.get_dir_contents(source, ref=sha)
        for content in contents:
            logger.info("Downloading %s", content.path)
            if content.type == 'dir':
                download_directory(repository, sha, content.path, target)
            else:
                path = content.path
                contents = repository.get_contents(path, ref=sha)
                data = base64.b64decode(contents.content)
                destination = os.path.join(target, path)
                logger.debug("Destination Path: %s", destination)
                makedirs(os.path.join(target, os.path.dirname(path)))
                output = open(destination, "w")
                output.write(data)
                output.close()
    except (GithubException, IOError) as exception:
        logger.error('Error downloading %s: %s', content.path, exception)
        raise GithubException("Failed to download the resource %s", source)


def get_sha(repository, tag):
    """
    Get the  unique ID against the commit of a given tag or branch. A commit,
    or "revision", is an individual change to a file (or set of files). It's like
    when you save a file, except with Git, every time you save it creates a unique
    ID (a.k.a. the "SHA" or "hash") that allows you to keep record of what changes
    were made when and by who.

    :param: repository (str): Git repository name hosted on GitHub server.
    :param: tag (str): Name of branch or tag name of the Git repository.
    :returns: sha (str): Absolute path of the target filename
    :raises: ValueError: If no Tag or Branch exists with that name
    """
    branches = repository.get_branches()
    matched_branches = [match for match in branches if match.name == tag]

    if matched_branches:
        return matched_branches[0].commit.sha

    tags = repository.get_tags()
    matched_tags = [match for match in tags if match.name == tag]

    if not matched_tags:
        raise ValueError('No Tag or Branch exists with that name')
    return matched_tags[0].commit.sha


def resolve_target(source, target):
    """
    Resolve the target path with source value. If the target is a
    valid filename it would be returned as such. If the target is a
    valid directory, name of the file would be extracted from the source
    path and created the final absolute path of the target filename.

    :param: source (str): Absolute path of the source filename in GitHub
    :param: target (str): Path of filename of directory name of the target
    :returns: target (str): Absolute path of the target filename
    :raises: None
    """
    if os.path.isdir(target):
        filename = os.path.basename(source)
        return os.path.join(target, filename)
    else:
        return target


def makedirs(path):
    """
    Create a leaf directory and all intermediate ones. Ignores the error
     if the give path (absolute path) exists on the local file system.

    :param (str) path: None
    :returns: None
    :raises: None
    """
    try:
        os.makedirs(path)
    except OSError as err:
        if err.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def get_options(args):
    """
    Get the command-line options for executing each commands.

    :param: args
    :returns: map options: Options supplied from command-line
    :raises: None
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--verbose', help="Enable debug level logging", action="store_const",
        dest="logging_level", const=logging.DEBUG, default=logging.INFO)
    parser.add_argument(
        '--quiet', help="Make little or no noise during the file transfer",
        action="store_const", dest="logging_level", const=logging.CRITICAL)
    subparsers = parser.add_subparsers(dest='command')
    fetch = subparsers.add_parser('fetch', help='Fetch file or directory')
    fetch.add_argument(
        '--hostname', required=False,
        help='Hostname of your GitHub server')
    fetch.add_argument(
        '--auth-token', required=True,
        help='A personal access token to authenticate to GitHub')
    fetch.add_argument(
        '--owner', required=False,
        help='Owner of the Git repository hosted on GitHub')
    fetch.add_argument(
        '--username', required=False,
        help='Username to authenticate GitHub server')
    fetch.add_argument(
        '--password', required=False,
        help='Password to authenticate GitHub server')
    fetch.add_argument(
        '--repository', required=True,
        help='Name of GitHub repository')
    fetch.add_argument(
        '--branch', required=False,
        help='Name of branch; a pointer to a snapshot of your changes')
    fetch.add_argument(
        '--tag', required=False,
        help='Name of tag; a version of a particular branch at a moment in time')
    fetch.add_argument(
        '--path', required=True,
        help='A specific file or directory path in your repository to download')
    fetch.add_argument(
        '--type', required=True,
        help='Indicates the given path is a file or directory')
    fetch.add_argument(
        '--destination', required=True,
        help='Destination directory path to download the file(s)')
    fetch.add_argument(
        "--http-ssl-verify", type=str_to_bool, nargs='?', const=True, default=True,
        help='Boolean flag to enable or disable the SSL certificate verification')
    options = parser.parse_args(args)
    return options


def str_to_bool(value):
    """
    Convert the string representation of a boolean value to boolean.
    Returns True the input value is 'yes', 'true', 't', 'y', '1' and False
    if the 'no', 'false', 'f', 'n', '0'.

    :param str value: string representation of a boolean value
    :returns: True or False based on the input value.
    :raises: ArgumentTypeError
    """
    if isinstance(value, bool):
        return value
    if value.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif value.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def get_branch_or_tag(options):
    """
    Get the value of branch or tag from the given list of options. If the
    value of branch option is provided in the commandline, that value would be
    returned. If the value of tag is provided with branch, branch name would be
    returned. If the value of tag is provided without branch, tag name would be
    returned. Branch name is considered as master if no value for branch or tag
    is provided in commandline.

    :param str hostname: Hostname to construct the API endpoint url.
    :returns str: Provided branch name, tag name or master by default.
    :raises: None
    """
    if options.branch:
        return options.branch
    elif options.tag:
        return options.tag
    return "master"


def get_base_url(hostname):
    """
    Constructs the GitHub API url with the given hostname.

    :param str hostname: Hostname to construct the API endpoint url.
    :returns: None
    :raises: None
    """
    if hostname and hostname.startswith('http'):
        return hostname
    else:
        return "https://{hostname}/api/v3".format(hostname=hostname)
    return hostname


def get_github(options):
    """
    Constructs the GitHub instance for fetch operation.

    :param options: Options to be used to establish the connection.
    :returns: Github instance
    :raises: GithubException
    """
    if options.hostname and options.auth_token:
        base_url = get_base_url(options.hostname)
        return Github(base_url=base_url, login_or_token=options.auth_token,
                      verify=options.http_ssl_verify)
    elif options.hostname and options.username and options.password:
        base_url = get_base_url(options.hostname)
        return Github(base_url=base_url, login_or_token=options.username,
                      password=options.password, verify=options.http_ssl_verify)
    elif not options.hostname and options.auth_token:
        return Github(options.auth_token)
    elif not options.hostname and options.username and options.password:
        return Github(options.username, options.password)
    else:
        raise GithubException("Unable to authenticate GitHub server!")


def fetch(options):
    """
    Fetch a specific file, folder or directory from a remote Git repository
    hosted on GitHub.

    :param map options: Options supplied from command-line to fetch the file/dir.
    :returns: None
    :raises: ValueError
    """
    base_url = get_base_url(options.hostname)
    branch_or_tag = get_branch_or_tag(options)

    logger.debug('base_url: %s', base_url)
    logger.debug('branch_or_tag: %s', branch_or_tag)
    logger.debug('http_ssl_verify: %s', options.http_ssl_verify)
    logger.debug('type: %s', options.type)

    github = None
    repository = None

    github = get_github(options)

    if options.hostname:
        organizations = github.get_user().get_orgs()
        logger.debug('github.get_user(): %s', github.get_user())
        logger.debug('organizations.totalCount: %s', organizations.totalCount)
        organization = organizations[0]
        logger.debug('organization: %s', organization)
        repository = organization.get_repo(options.repository)
    else:
        repository = github.get_repo("{owner}/{repository}".format(
            owner=options.owner, repository=options.repository))

    sha = get_sha(repository, branch_or_tag)
    logger.debug('sha or hash: %s', sha)

    if options.type.lower() in ('f', 'file'):
        destination = resolve_target(options.path, options.destination)
        logger.debug('destination: %s', destination)
        download_file(repository, sha, options.path, destination)
    elif options.type.lower() in ('d', 'dir', 'directory'):
        destination = options.destination
        logger.debug('destination: %s', destination)
        download_directory(repository, sha, options.path, destination)
    else:
        raise ValueError('Value of --type should be either file or directory')


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    options = get_options(sys.argv[1:])
    logger.setLevel(level=options.logging_level)

    if options.command == 'fetch':
        fetch(options)
    else:
        raise ValueError('Unknown option %s', options.command)
    logger.info('Task completed.')


if __name__ == '__main__':
    main()
