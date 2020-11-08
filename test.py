"""
This is the script used during development.
"""

import sys
import time
import pprint
import requests
import argparse

from typing import Any, AnyStr, Callable

#: The root URL for the API.
URL = 'http://127.0.0.1:5000/'

#: The default profile to check.
PROFILE = 'mailchimp'


def main(argv: list):
    # Create a command-line argument parser.
    parser = argparse.ArgumentParser(prog=argv[0], description=__doc__, add_help=False)

    # Optional arguments.
    optional = parser.add_argument_group(title="Optional Arguments")
    optional.add_argument('-p', '--profile', required=False, default=PROFILE, help="The team or organization to profile.")
    optional.add_argument('-h', '--help', action='help', help="Show this help message and exit.")

    # Parse the command-line arguments.
    parsed = parser.parse_args(argv[1:])
    profile = parsed.profile

    # Get the team profile.
    profile = get_profile(profile)

    pprint.pprint(profile)


def get_profile(profile: AnyStr) -> dict:
    """
    Get the profile for the team or organization.
    :param profile: is the team or organization to look up.
    :return:
    """

    # Build the URL for the request.
    url = f'{URL}/profiles/{profile}'

    return requests.get(url).json()


if __name__ == '__main__':
    main(sys.argv)
