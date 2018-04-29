import json
import uuid
from copy import deepcopy

from participation.use_cases import get_participation
from tests.fixtures import (
    active_session,
    client,
    inactive_session,
)


MOCK_PARTICIPATION = {
    'user_id': 'MY_USER_ID',
    'name': 'Not Mordred',
    'preferences': [str(uuid.uuid4()) for i in range(5)],
}


def test_create_participation(
    client,
    active_session,
):
    response = post_participation(
        client,
        active_session['session_id'],
        data=MOCK_PARTICIPATION,
    )

    data = json.loads(response.data)
    assert data['preferences'] == MOCK_PARTICIPATION['preferences']
    assert data['user_id'] == MOCK_PARTICIPATION['user_id']
    assert get_participation(
        active_session['session_id'],
        data['user_id'],
    ) == data


def test_create_participation_without_preferences(client, active_session):
    participation = deepcopy(MOCK_PARTICIPATION)
    del participation['preferences']
    response = post_participation(
        client,
        active_session['session_id'],
        data=participation,
        expected_response=400,
    )


def test_create_participation_with_empty_preferences(client, active_session):
    participation = deepcopy(MOCK_PARTICIPATION)
    participation['preferences'] = []
    response = post_participation(
        client,
        active_session['session_id'],
        data=participation,
    )
    data = json.loads(response.data)

    assert data['preferences'] == []


def test_create_participation_with_empty_user_id(client, active_session):
    participation = deepcopy(MOCK_PARTICIPATION)
    participation['user_id'] = ''
    response = post_participation(
        client,
        active_session['session_id'],
        data=participation,
        expected_response=400,
    )


def test_create_participation_non_existing_session(client):
    response = post_participation(
        client,
        'I DO NOT EXIST',
        data=MOCK_PARTICIPATION,
        expected_response=404,
    )


def test_create_participation_for_inactie_session(client, inactive_session):
    response = post_participation(
        client,
        inactive_session['session_id'],
        data=MOCK_PARTICIPATION,
        expected_response=403,
    )


# Helpers
def post_participation(client, session_id, data={}, expected_response=200):
    response = client.post(
        '/session/{}/participation/'.format(session_id),
        data=json.dumps(data),
        content_type='application/json'
    )
    assert response.status_code == expected_response
    return response
