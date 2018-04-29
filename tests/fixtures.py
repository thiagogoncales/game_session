import pytest

import app
from game.use_cases import create_game
from participation.use_cases import add_participation
from session.use_cases import create_session


@pytest.fixture
def client():
    return app.app.test_client()


@pytest.fixture
def active_session():
    return create_session(is_active=True)


@pytest.fixture
def inactive_session():
    return create_session(is_active=False)


@pytest.fixture
def games_for_active_session(active_session):
    session_id = active_session['session_id']
    games = []
    for i in range(5):
        games.append(create_game(
            session_id,
            name='Game {}'.format(i),
            min_players=i,
            max_players=i+5,
        ))

    return games


@pytest.fixture
def session_for_game_session():
    return create_session(is_active=True)


@pytest.fixture
def game_with_min_participation_game_session(session_for_game_session):
    session_id = session_for_game_session['session_id']
    min_players = 5
    max_players = min_players + 5
    game_name = 'game_with_min_participation'

    return _get_game_session(
        session_id,
        game_name,
        min_players,
        max_players,
        min_players,
    )


@pytest.fixture
def game_with_max_participation_game_session(
    session_for_game_session,
):
    session_id = session_for_game_session['session_id']
    min_players = 5
    max_players = min_players + 5
    game_name = 'game_with_max_participation'

    return _get_game_session(
        session_id,
        game_name,
        min_players,
        max_players,
        max_players,
    )


@pytest.fixture
def game_with_not_enough_participation_game_session(session_for_game_session):
    session_id = session_for_game_session['session_id']
    min_players = 5
    max_players = min_players + 5
    game_name = 'game_with_not_enough_participation'

    return _get_game_session(
        session_id,
        game_name,
        min_players,
        max_players,
        min_players - 1,
    )

    return _get_game_session(game, [])


@pytest.fixture
def game_with_more_than_max_participation_game_session(
    session_for_game_session,
):
    session_id = session_for_game_session['session_id']
    min_players = 5
    max_players = min_players + 5
    game_name = 'game_with_more_than_max_participation'

    return _get_game_session(
        session_id,
        game_name,
        min_players,
        max_players,
        max_players + 1,
    )


def _get_game_session(
    session_id,
    game_name,
    min_players,
    max_players,
    number_of_interested_players,
):
    game = create_game(
        session_id,
        name=game_name,
        min_players=min_players,
        max_players=max_players,
    )

    participation = [
        add_participation(
            session_id,
            'user_for_game_{}_{}'.format(game_name, i),
            'Player for game {} #{}'.format(game_name, i),
            [game['game_id']],
        )
        for i in range(number_of_interested_players)
    ]

    return {
        'game_id': game['game_id'],
        'players': [player['user_id'] for player in participation],
    }
