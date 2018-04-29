import pytest

import app
from game.use_cases import create_game
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
