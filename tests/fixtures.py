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
def game_with_participation(active_session):
    session_id = active_session['session_id']
    min_players = 5
    max_players = min_players + 5
    game_name = 'game_with_participation'

    return create_game(
        session_id,
        name=game_name,
        min_players=min_players,
        max_players=max_players,
    )


@pytest.fixture
def min_participation_for_game_with_participation(
    active_session,
    game_with_participation,
):
    return _add_participation_for_game(
        active_session,
        game_with_participation,
        game_with_participation['min_players'],
    )


@pytest.fixture
def max_participation_for_game_with_participation(
    active_session,
    game_with_participation,
):
    return _add_participation_for_game(
        active_session,
        game_with_participation,
        game_with_participation['max_players'],
    )

@pytest.fixture
def less_than_min_participation_for_game_with_participation(
    active_session,
    game_with_participation,
):
    return _add_participation_for_game(
        active_session,
        game_with_participation,
        game_with_participation['min_players'] - 1,
    )


@pytest.fixture
def more_than_max_participation_for_game_with_participation(
    active_session,
    game_with_participation,
):
    return _add_participation_for_game(
        active_session,
        game_with_participation,
        game_with_participation['max_players'] + 1,
    )

def _add_participation_for_game(session, game, number_of_interested_players):
    game_name = game['name']
    return [
        add_participation(
            session['session_id'],
            'user_for_game_{}_{}'.format(game_name, i),
            'Player for game {} #{}'.format(game_name, i),
            [game['game_id']],
        )
        for i in range(number_of_interested_players)
    ]
