import json

from session.use_cases import (
    get_session,
)
from tests.fixtures import (
    active_session,
    client,
    inactive_session,
)


def test_create_new_session(client):
    response = post_session_list(client)
    data = json.loads(response.data)

    assert data['is_active']
    assert get_session(data['session_id']) == data


def test_modify_session(client, active_session):
    response = put_session_detail(
        client,
        active_session['session_id'],
        data={'is_active': False},
    )
    data = json.loads(response.data)

    assert data['session_id'] == active_session['session_id']
    assert get_session(data['session_id']) == data
    assert data['is_active'] == False


def test_modify_non_existent_session(client):
    response = put_session_detail(
        client,
        'I DO NOT EXIST',
        data={'is_active': False},
        expected_response=404,
    )


def test_modify_non_existent_attribute(client, active_session):
    response = put_session_detail(
        client,
        active_session['session_id'],
        data={'NOT A REAL ATTRIBUTE': False},
        expected_response=400,
    )


def test_get_session(client, active_session):
    response = get_session_detail(
        client,
        active_session['session_id'],
    )
    data = json.loads(response.data)

    assert data['session_id'] == active_session['session_id']


def test_get_non_existing_session(client, active_session):
    response = get_session_detail(
        client,
        'I DO NOT EXIST',
        expected_response=404,
    )


################ Helpers ################
def post_session_list(client, data={}, expected_response=200):
    response = client.post(
        '/session/',
        data=json.dumps(data),
        content_type='application/json'
    )
    assert response.status_code == expected_response
    return response


def put_session_detail(client, session_id, data={}, expected_response=200):
    response = client.put(
        '/session/{}/'.format(session_id),
        data=json.dumps(data),
        content_type='application/json'
    )
    assert response.status_code == expected_response
    return response

def get_session_detail(client, session_id, expected_response=200):
    response = client.get(
        '/session/{}/'.format(session_id),
        content_type='application/json'
    )
    assert response.status_code == expected_response
    return response
