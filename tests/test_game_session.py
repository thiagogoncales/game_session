import json

from session.use_cases import (
    get_session,
    set_game_session_active_status,
)
from tests.fixtures import (
    active_session,
    client,
    game_with_participation,
    min_participation_for_game_with_participation,
    max_participation_for_game_with_participation,
    less_than_min_participation_for_game_with_participation,
    more_than_max_participation_for_game_with_participation,
)


def test_get_game_session_on_active_session(
    client,
    active_session,
):
    get_game_session_detail(
        client,
        active_session['session_id'],
        expected_response=403,
    )


def test_get_game_session_min_participation(
    client,
    active_session,
    game_with_participation,
    min_participation_for_game_with_participation,
):
    session_id = active_session['session_id']
    set_game_session_active_status(session_id, False)
    response = get_game_session_detail(
        client,
        session_id,
    )

    data = json.loads(response.data)
    game_sessions = data['game_sessions']

    assert {
        'game_id': game_with_participation['game_id'],
        'players': [
            player['user_id']
            for player in min_participation_for_game_with_participation
        ],
    } in game_sessions


def test_get_game_session_max_participation(
    client,
    active_session,
    game_with_participation,
    max_participation_for_game_with_participation,
):
    session_id = active_session['session_id']
    set_game_session_active_status(session_id, False)
    response = get_game_session_detail(
        client,
        session_id,
    )

    data = json.loads(response.data)
    game_sessions = data['game_sessions']

    assert {
        'game_id': game_with_participation['game_id'],
        'players': [
            player['user_id']
            for player in max_participation_for_game_with_participation
        ],
    } in game_sessions


def test_get_game_session_less_than_min_participation(
    client,
    active_session,
    game_with_participation,
    less_than_min_participation_for_game_with_participation,
):
    session_id = active_session['session_id']
    set_game_session_active_status(session_id, False)
    response = get_game_session_detail(
        client,
        session_id,
    )

    data = json.loads(response.data)
    game_sessions = data['game_sessions']

    assert next((
        game_session
        for game_session in game_sessions
        if game_session['game_id'] == game_with_participation['game_id']
    ), False) == False


def test_get_game_session_more_than_max_participation(
    client,
    active_session,
    game_with_participation,
    more_than_max_participation_for_game_with_participation,
):
    session_id = active_session['session_id']
    set_game_session_active_status(session_id, False)
    response = get_game_session_detail(
        client,
        session_id,
    )

    data = json.loads(response.data)
    game_sessions = data['game_sessions']

    assert len(next((
        game_session
        for game_session in game_sessions
        if game_session['game_id'] == game_with_participation['game_id']
    ))['players']) == game_with_participation['max_players']


def get_game_session_detail(client, session_id, expected_response=200):
    response = client.get(
        '/session/{}/game_session/'.format(session_id),
        content_type='application/json'
    )
    assert response.status_code == expected_response
    return response
