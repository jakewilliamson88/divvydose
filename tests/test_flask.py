import os
import tempfile

import pytest
import app.routes

app = app.routes.app


@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def test_health_check(client):
    """ Test the /health-check endpoint """
    rv = client.get('/health-check')
    assert rv.status_code == 200
    assert b'Ok' in rv.data


def test_profiles(client):
    """ Test the /profiles endpoint """

    # Test response for MailChimp
    rv = client.get('/profiles/mailchimp')
    dt = rv.get_json()
    assert rv.status_code == 200
    assert dt['organization'] == 'mailchimp'  # Found in Github
    assert dt['team'] == 'mailchimp'  # Found in Bitbucket

    # Test PyGame
    rv = client.get('/profiles/pygame')
    dt = rv.get_json()
    assert rv.status_code == 200
    assert dt['organization'] == 'pygame'  # Found in Github
    assert dt['team'] == 'pygame'  # Found in Bitbucket

    # Test an empty return value.
    rv = client.get('/profiles/bogusrepo')
    dt = rv.get_json()
    assert rv.status_code == 200

    messages = dt['messages']
    assert messages['bitbucket'] == "No workspace with identifier 'bogusrepo'."
    assert messages['github'] == 'Not Found'
