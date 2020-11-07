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


def timed(func: Callable) -> Callable:
    """
    Time function executions.
    :param func: is the decorated function.
    :return: function
    """

    def wrapped(*args: list, **kwargs: dict) -> Any:
        """
        The replacement for the decorated function.
        :param args: list of args
        :param kwargs: dict of keyword args.
        :return: Any
        """

        # Record the start time.
        start = time.time()

        # Call the decorated function.
        retval = func(*args, **kwargs)

        # Report execution time.
        print(" - {:.4f}s".format(time.time() - start))

        return retval

    return wrapped()


def main(argv: list):
    # Create a command-line argument parser.
    parser = argparse.ArgumentParser(prog=argv[0], description=__doc__, add_help=False)

    # Optional arguments.
    optional = parser.add_argument_group(title="Optional Arguments")
    optional.add_argument('-t', '--team', required=False, default=PROFILE, help="The team or organization to profile.")
    optional.add_argument('-h', '--help', action='help', help="Show this help message and exit.")

    # Parse the command-line arguments.
    parsed = parser.parse_args(argv[1:])
    team = parsed.team

    # Get the team profile.
    profile = get_profile(team)

    pprint.pprint(profile)


def get_profile(team: AnyStr) -> dict:
    """
    Get the profile for the team or organization.
    :param team:
    :return:
    """

    # Build the URL for the request.
    url = f'{URL}/profiles/{team}'

    return requests.get(url).json()


if __name__ == '__main__':
    main(sys.argv)
