import json
from copy import deepcopy

from game.use_cases import get_game
from session.use_cases import create_session
from tests.fixtures import (
    active_session,
    client,
    games_for_active_session,
    inactive_session,
)


MOCK_GAME = {
    'name': 'Avalon',
    'min_players': 7,
    'max_players': 10,
}


def test_create_new_game(client, active_session):
    response = post_game(
        client,
        active_session['session_id'],
        data=MOCK_GAME,
    )
    data = json.loads(response.data)

    assert get_game(data['session_id'], data['game_id']) == data


def test_create_new_game_non_existing_session(client, inactive_session):
    response = post_game(
        client,
        'I DO NOT EXIST',
        data=MOCK_GAME,
        expected_response=404,
    )


def test_create_new_game_inactive_session(client, inactive_session):
    response = post_game(
        client,
        inactive_session['session_id'],
        data=MOCK_GAME,
        expected_response=403,
    )


def test_create_new_game_invalid_data(client, active_session):
    response = post_game(
        client,
        active_session['session_id'],
        data={},
        expected_response=400,
    )


def test_create_new_game_empty_name(client, active_session):
    data = deepcopy(MOCK_GAME)
    data['name'] = ''
    response = post_game(
        client,
        active_session['session_id'],
        data=data,
        expected_response=400,
    )


def test_create_new_game_max_players_less_than_min(client, active_session):
    data = deepcopy(MOCK_GAME)
    data['min_players'], data['max_players'] = \
        data['max_players'], data['min_players']
    response = post_game(
        client,
        active_session['session_id'],
        data=data,
        expected_response=400,
    )


def test_get_all_games(client, active_session, games_for_active_session):
    response = get_game_list(client, active_session['session_id'])
    data = json.loads(response.data)

    assert len(data) == len(games_for_active_session)
    for game in games_for_active_session:
        assert game in data


# Helpers
def post_game(client, session_id, data={}, expected_response=200):
    response = client.post(
        '/session/{}/game/'.format(session_id),
        data=json.dumps(data),
        content_type='application/json'
    )
    assert response.status_code == expected_response
    return response


def get_game_list(client, session_id, expected_response=200):
    response = client.get(
        '/session/{}/game/'.format(session_id),
        content_type='application/json'
    )
    assert response.status_code == expected_response
    return response
