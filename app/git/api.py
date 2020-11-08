"""
This module implements API call functionality.
"""

from typing import AnyStr
import requests
from collections import defaultdict


class Api:

    @staticmethod
    def _call(method: AnyStr, url: AnyStr, headers: dict = None) -> dict:
        """

        :param method: is the HTTP request method
        :param url: is the URL to make the request to
        :return: the API response as a dict.
        """

        request = {
            'GET': requests.get
        }[method]

        response = request(url, headers=headers)

        return response.json()


class Bitbucket(Api):
    """
    The ``Bitbucket`` class implements the Bitbucket API calls.
    """

    # The URI for the Bitbucket API.
    uri = 'https://api.bitbucket.org/2.0'

    def workspace_repositories(self, workspace: AnyStr, page: int = 1, pagelen: int = 100) -> dict:
        """
        Return the workspace repositories as a dict.
        :param pagelen: is the number of results to return per page.
        :param page: is the result page.
        :param workspace: is the workspace to query.
        :return: dict
        """

        # Get the URL for the request.
        endpoint = f'/repositories/{workspace}?page={page}&pagelen={pagelen}'
        url = f'{Bitbucket.uri}{endpoint}'

        return self._call('GET', url)

    def profile(self, team: AnyStr) -> dict:
        """
        Build a profile for the team.
        :param team: is the team name
        :return: dict
        """

        # Get the workspace repositories for the team.
        repos = self.workspace_repositories(team)

        # Bitbucket returns an error for workspaces that are not found.
        if repos.get('type') == 'error':
            return repos

        # Placeholder for profile values.
        public_repos = 0
        language_list = set()
        language_counts = defaultdict(lambda: 0)

        for repo in repos['values']:

            # Count public repos
            if not repo['is_private']:
                public_repos += 1

            # Track the languages
            language = repo.get('language', 'unknown')
            language_list.add(language)
            language_counts[language] += 1

        return {
            'team': team,
            'repositories': {
                'public_count': public_repos,
            },
            'languages': {
                'list': list(language_list),
                'count': dict(language_counts)
            }
        }


class Github(Api):
    """
    The ``Github`` class implements the Github API calls.
    """

    # The URI For the github API.
    uri = 'https://api.github.com'

    def organization_repositories(self, organization: AnyStr) -> dict:
        """
        Fetch the organization details.
        :param organization: is the organization to fetch.
        :return: dict
        """

        # The request headers.
        headers = {
            'Accept': 'application/vnd.github.mercy-preview+json'
        }

        # The API endpoint.
        endpoint = f'/orgs/{organization}/repos'
        url = f'{Github.uri}{endpoint}'

        return self._call('GET', url, headers=headers)

    def profile(self, organization: AnyStr) -> dict:
        """
        Build a profile for the organization.
        :param organization:
        :return: dict
        """

        # Get the organization repos.
        repos = self.organization_repositories(organization)

        # repost will be a list if the call was successful.
        if isinstance(repos, dict):
            return repos

        # Placeholders for profile values.
        public_repos = 0
        forked_repos = 0
        original_repos = 0
        language_list = set()
        language_counts = defaultdict(lambda: 0)
        watchers = 0
        topic_list = set()
        topic_counts = defaultdict(lambda: 0)

        for repo in repos:

            # Count public repos.
            if not repo.get('private'):
                public_repos += 1

            # Count forks.
            if repo.get('fork', False):
                forked_repos += 1
            else:
                public_repos += 1

            # Get watchers.
            watchers += repo.get('watchers', 0)

            # Track the languages.
            language = repo.get('language', 'unknown') or 'unknown'
            language = language.lower()
            language_list.add(language)
            language_counts[language] += 1

            # Get the repo topics.
            topics = repo.get('topics', [])
            for topic in topics:
                topic_list.add(topic)
                topic_counts[topic] += 1

        return {
            'organization': organization,
            'repositories': {
                'public_count': public_repos,
                'forked': forked_repos,
                'original': original_repos
            },
            'languages': {
                'list': list(language_list),
                'count': dict(language_counts)
            },
            'topics': {
                'list': list(topic_list),
                'count': dict(topic_counts)
            },
            'watchers': watchers
        }
