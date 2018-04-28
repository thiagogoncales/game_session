import json

from session.use_cases import (
    get_session,
)
from tests.fixtures import client


def test_create_new_session(client):
    response = post_session(client)
    data = json.loads(response.data)

    assert data['is_active']
    assert get_session(data['session_id']) == data


# Helpers
def post_session(client, data={}, expected_response=200):
    response = client.post(
        '/session/',
        data=data,
    )
    assert response.status_code == expected_response
    return response
