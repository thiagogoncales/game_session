import json

from tests.fixtures import client

from session.constants import SESSION_OPEN
from session.use_cases import (
    get_session,
)


def test_create_new_session(client):
    response = post_session(client)
    data = json.loads(response.data)

    assert 'id' in data
    assert data['state'] == SESSION_OPEN
    assert get_session(data['id']) == data


def test_get_all_sessions(client):
    post_response = post_session(client)
    created_session = json.loads(post_response.data)

    response = get_session_list(client)
    sessions = json.loads(response.data)

    assert created_session in sessions


# Helpers
def post_session(client, data={}, expected_response=200):
    response = client.post(
        '/session/',
        data=data,
    )
    assert response.status_code == expected_response
    return response


def get_session_list(client, expected_response=200):
    response = client.get(
        '/session/',
    )
    assert response.status_code == expected_response
    return response
