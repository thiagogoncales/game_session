import json

from session.use_cases import (
    get_session,
    set_game_session_active_status,
)
from tests.fixtures import (
    client,
    game_with_max_participation_game_session,
    game_with_min_participation_game_session,
    game_with_not_enough_participation_game_session,
    session_for_game_session,
)


def test_get_game_session_on_active_session(
    client,
    session_for_game_session,
):
    get_game_session_detail(
        client,
        session_for_game_session['session_id'],
        expected_response=403,
    )


def test_get_game_sessions(
    client,
    session_for_game_session,
    game_with_max_participation_game_session,
    game_with_min_participation_game_session,
    game_with_not_enough_participation_game_session,
):
    session_id = session_for_game_session['session_id']
    set_game_session_active_status(session_id, False)
    response = get_game_session_detail(
        client,
        session_id
    )

    data = json.loads(response.data)
    game_sessions = data['game_sessions']

    assert data['session_id'] == session_id
    assert game_with_min_participation_game_session in game_sessions
    assert game_with_max_participation_game_session in game_sessions
    assert next((
            game_session
            for game_session in game_sessions
            if game_session['game_id'] == \
                game_with_not_enough_participation_game_session['game_id']
    ), False) == False

    # TODO: Add coverage after fixing bug
    #assert game_with_more_than_max_participation_game_session in game_sessions


def get_game_session_detail(client, session_id, expected_response=200):
    response = client.get(
        '/session/{}/game_session/'.format(session_id),
        content_type='application/json'
    )
    assert response.status_code == expected_response
    return response
