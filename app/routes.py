import logging

import flask
from flask import Response, jsonify

from app.git.api import Bitbucket, Github

app = flask.Flask("user_profiles_api")
logger = flask.logging.create_logger(app)
logger.setLevel(logging.INFO)


@app.route("/health-check", methods=["GET"])
def health_check():
    """
    Endpoint to health check API.
    """
    app.logger.info("Health Check")
    return Response("Ok", status=200)


@app.route('/profiles/<profile>', methods=['GET'])
def profiles(profile):
    """
    Fetch profile data from the Bitbucket and Github APIs.
    :param profile: is the profile to aggregate.
    :return: JSON
    """

    # Log every request.
    app.logger.info(f"Fetching data for '{profile}'")

    # Get the bitbucket profile.
    bitbucket = Bitbucket()
    bb_profile = bitbucket.profile(profile)

    # Get the github profile.
    github = Github()
    gh_profile = github.profile(profile)

    # Get the languages.
    bb_languages = bb_profile.get('languages', {})
    gh_languages = gh_profile.get('languages', {})

    # Aggregate language counts.
    bb_language_counts = bb_languages.get('count', {})
    gh_language_counts = gh_languages.get('count', {})
    ag_language_counts = {
        language: bb_language_counts.get(language, 0) + gh_language_counts.get(language, 0)
        for language in set(bb_language_counts).union(set(gh_language_counts))
    }

    # Aggregate the language lists.
    bb_language_list = bb_languages.get('list', [])
    gh_language_list = gh_languages.get('list', [])
    ag_language_list = list(set(bb_language_list+gh_language_list))

    # Get the profile repos.
    bb_repos = bb_profile.get('repositories', {})
    gh_repos = gh_profile.get('repositories', {})
    ag_repos = bb_repos.get('public_count', 0) + gh_repos.get('public_count', 0)

    # Aggregate the original repo counts.
    bb_original = bb_repos.get('original', 0)
    gh_original = 0
    ag_original = bb_original+gh_original

    # Handle github topics.
    gh_topics = gh_profile.get('topics', {})
    gh_topics_list = gh_topics.get('list', [])
    gh_topics_count = gh_topics.get('count', {})

    # Merge the profiles.
    merged_profile = {
        'team': bb_profile.get('team'),
        'organization': gh_profile.get('organization'),
        'repositories': {
            'public_count': {
                'total': ag_repos,
                'bitbucket': bb_repos.get('public_count', 0),
                'github': gh_repos.get('public_count', 0)
            },
            'forked': gh_repos.get('forked', 0),
            'original': {
                'total': ag_original,
                'bitbucket': bb_original,
                'github': gh_original
            },
        },
        'languages': {
            'list': ag_language_list,
            'count': ag_language_counts
        },
        'topics': {
            'list': gh_topics_list,
            'count': gh_topics_count
        },
        'messages': {
            'github': gh_profile.get('message'),
            'bitbucket': bb_profile.get('error', {}).get('message')
        }
    }

    return jsonify(merged_profile)
