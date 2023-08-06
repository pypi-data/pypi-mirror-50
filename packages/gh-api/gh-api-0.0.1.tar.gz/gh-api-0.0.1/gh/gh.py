"""
gh
==========
License: BSD, see LICENSE for more details.
"""

import argparse
import json
import logging as log  # for verbose output
import os

import requests
from appdirs import user_cache_dir
from cachecontrol import CacheControl
from cachecontrol.caches.file_cache import FileCache

from .__about__ import __version__


def api_call(endpoint, method, field_name = None):
    endpoint = endpoint.lstrip('/')
    headers = {}
    cache_dir = user_cache_dir("gh")
    log.info("Using cache directory: {}.".format(cache_dir))

    api_token = os.getenv("GITHUB_API_TOKEN")
    if api_token:
        log.info("Using API token")
        headers['Authorization'] = "token {}".format(api_token)

    with CacheControl(requests.Session(),
                      cache=FileCache(cache_dir)) as s:
        s.headers.update(headers)

        if method == 'GET':
            r = s.get(
                'https://api.github.com/{}'.format(endpoint),
                headers=headers)
            rj = r.json()
            if field_name:
                if field_name in rj:
                    return(rj[field_name])
                else:
                    exit(23)
            else:
                return json.dumps(r.json())
            if r.status_code == 404:
                exit(22)
    s.close()



def main():
    parser = argparse.ArgumentParser(description='Low-level GitHub API request interface.')
    parser.add_argument('endpoint', metavar='ENDPOINT',
                        help='The GitHub API endpoint to send the HTTP request to (default: "/")')
    parser.add_argument('--verbose', dest='verbose', action='store_true')
    parser.add_argument('--version', action='version',
                        version='%(prog)s {version}'.format(version=__version__))
    parser.add_argument('-X', '--method', choices=['GET', 'POST'], metavar='METHOD',
                        help='The HTTP method to use for the request (default: "GET")')
    parser.add_argument('--field-name', '-f',
                        help='Output value of a given field from JSON data')

    parser.set_defaults(endpoint='/', method='GET')
    args = parser.parse_args()

    if args.verbose:
        log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
        log.info("Verbose output.")
    else:
        log.basicConfig(format="%(levelname)s: %(message)s")

    output = api_call(args.endpoint, args.method, args.field_name)

    print(output)

if __name__ == "__main__":
    main()
