#!python

import os
import sys
import tempfile
import requests
import tarfile
from gitignore import GitIgnore


class ShipaException(Exception):
    pass


class RepositoryFolder(object):
    IGNORE_FILENAME = '.shipaignore'

    def __init__(self, directory, verbose=False):
        assert directory is not None
        assert verbose is not None

        self.directory = directory
        self.verbose = verbose

        ignore_path = os.path.join(directory, self.IGNORE_FILENAME)
        lines = None
        if os.path.isfile(ignore_path) is True:
            with open(ignore_path, 'r') as f:
                lines = f.readlines()
        self.shipa_ignore = GitIgnore(lines or [])

    def create_tarfile(self):

        os.chdir(self.directory)
        if self.verbose: print('Create tar archive:')

        def filter(info):
            if info.name.startswith('./.git'):
                return

            filename = info.name[2:]

            if self.shipa_ignore.match(filename):
                if self.verbose: print('IGNORE: ', filename)
                return

            if self.verbose: print('OK', filename)
            return info

        f = tempfile.TemporaryFile(suffix='.tar.gz')
        tar = tarfile.open(fileobj=f, mode="w:gz")
        tar.add(name='.',
                recursive=True,
                filter=filter)
        tar.close()
        f.seek(0)
        return f


class ShipaClient(object):

    def __init__(self, server, email=None, password=None, token=None, verbose=False):
        self.server = server
        if not server.startswith('http'):
            self.urlbase = 'http://{0}'.format(server)
        else:
            self.urlbase = server

        self.email = email
        self.password = password
        self.token = token
        self.verbose = verbose

    def auth(self):
        if self.email is None or self.password is None:
            raise ShipaException('Please, provide email and password')

        url = '{0}/users/{1}/tokens'.format(self.urlbase, self.email)
        params = {'password': self.password}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        r = requests.post(url, params=params, headers=headers)
        if self.verbose:
            print('Server response: ')
            print(r.text)

        if r.status_code != 200:
            raise ShipaException(r.text)

        self.token = r.json()['token']

    def deploy(self, appname, directory):
        folder = RepositoryFolder(directory, verbose=self.verbose)
        file = folder.create_tarfile()

        url = '{0}/apps/{1}/deploy'.format(self.urlbase, appname)
        headers = {"Authorization": "bearer " + self.token}

        files = {'file': file}
        body = {'kind': 'git'}
        r = requests.post(url, files=files, headers=headers, data=body)

        if self.verbose:
            print('Server response:')
            print(r.text)
            print (r.status_code)

        if r.status_code != 200:
            raise ShipaException(r.text)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Shipa CI tool')
    parser.add_argument('--directory',
                        help='directory to deploy (default .)',
                        default='.')
    parser.add_argument('--app', help='application name', required=True)
    parser.add_argument('--server',
                        help='shipa server, for example http://shipa-ci-integration.org:8080',
                        required=True)
    parser.add_argument('--email', help='user email')
    parser.add_argument('--password', help='user password')
    parser.add_argument('--token', help='token')
    parser.add_argument('--verbose', help='verbose output', default=False, action='store_true')
    args = parser.parse_args()

    try:
        client = ShipaClient(server=args.server,
                             email=args.email,
                             password=args.password,
                             token=args.token,
                             verbose=args.verbose)
        if args.token is None:
            client.auth()

        client.deploy(appname=args.app, directory=args.directory)

    except ShipaException as e:
        print('We have some a problem: {0}'.format(str(e)))
        sys.exit(1)
