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

from github import Github
from github import GithubException
from configurer import configure_logging

logger = configure_logging(logging.getLogger('pygithubctl'))


def download_file(repository, sha, source, target):
    logger.info('Fetching %s from %s', source, repository)
    try:
        contents = repository.get_contents(source, ref=sha)
        data = base64.b64decode(contents.content)
        output = open(target, "w")
        output.write(data)
        output.close()
    except (GithubException, IOError) as exception:
        logger.error('Error processing %s: %s', source, exception)


def download_directory(repository, sha, source, target):
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
                logger.debug("destination %s", destination)
                mkdirs(os.path.join(target, os.path.dirname(path)))
                output = open(destination, "w")
                output.write(data)
                output.close()
    except (GithubException, IOError) as exception:
        logger.error('Error processing %s: %s', content.path, exception)


def get_sha(repository, tag):
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
    if os.path.isdir(target):
        filename = os.path.basename(source)
        return os.path.join(target, filename)
    else:
        return target


def mkdirs(path):
    try:
        os.makedirs(path)
    except OSError as err:
        if err.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def get_options():
    """Get the command-line options for executing each commands.

    :param: None
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
    options = parser.parse_args()
    return options


def str_to_bool(value):
    if isinstance(value, bool):
        return value
    if value.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif value.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def get_branch_or_tag(options):
    branch_or_tag = "master"
    if options.branch:
        branch_or_tag = options.branch
    if options.tag:
        branch_or_tag = options.tag
    return branch_or_tag


def get_base_url(hostname):
    """Constructs the GitHub API url with the given hostname.

    :param str hostname: Hostname to construct the API endpoint url.
    :returns: None
    :raises: None

    """
    if hostname and hostname.startswith('http'):
        return hostname
    else:
        return "https://{hostname}/api/v3".format(hostname=hostname)
    return hostname


def fetch(options):
    """Fetch a specific file, folder or directory from a remote Git repository
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

    if options.hostname:
        github = Github(base_url=base_url, login_or_token=options.auth_token,
                        verify=options.http_ssl_verify)
        organizations = github.get_user().get_orgs()
        logger.debug('github.get_user(): %s', github.get_user())
        logger.debug('organizations.totalCount: %s', organizations.totalCount)
        organization = organizations[0]
        logger.debug('organization: %s', organization)
        repository = organization.get_repo(options.repository)
    else:
        github = Github(options.auth_token)
        repository = github.get_repo("{owner}/{repository}".format(
            owner=options.owner, repository=options.repository))

    sha = get_sha(repository, branch_or_tag)
    logger.debug('sha: %s', sha)

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
    options = get_options()
    logger.setLevel(level=options.logging_level)

    if options.command == 'fetch':
        fetch(options)
    else:
        raise ValueError('Unknown option %s', options.command)
    logger.info('Task completed.')


if __name__ == '__main__':
    main()
