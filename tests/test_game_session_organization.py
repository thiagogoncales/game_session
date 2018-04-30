import pytest

from session.game_session import (
    game_has_enough_interest,
    get_game_sessions,
)


@pytest.fixture
def games():
    return [
    {
        'game_id': 'Game ID {}'.format(i),
        'name': 'Game Name {}'.format(i),
        'min_players': i,
        'max_players': i + 5,
    } for i in range(1, 6)
]


def test_has_minimal_interest(games):
    game = games[0]
    interest = generate_interest(game['min_players'])
    assert game_has_enough_interest(game, interest) == True


def test_over_maximum_interest(games):
    game = games[0]
    interest = generate_interest(game['max_players'] + 1)
    assert game_has_enough_interest(game, interest) == True


def test_below_minimum_interest(games):
    game = games[0]
    interest = generate_interest(game['min_players'] - 1)
    assert game_has_enough_interest(game, interest) == False


def test_get_game_sessions_enough_players(games):
    game = games[-1]
    game_participation = create_participation(
        game['game_id'],
        game['min_players'],
    )

    game_sessions = get_game_sessions(games, game_participation)
    expected_game_session = {
        'game_id': game['game_id'],
        'game_name': game['name'],
        'players': [player['user_id'] for player in game_participation],
    }
    assert expected_game_session in game_sessions

def test_get_game_sessions_not_enough_players(games):
    game = games[-1]
    game_participation = create_participation(
        game['game_id'],
        game['min_players'] - 1,
    )

    game_sessions = get_game_sessions(games, game_participation)

    assert next((
        game_session
        for game_session in game_sessions
        if game_session['game_id'] == game['game_id']
    ), False) == False


def test_get_game_sessions_too_many_players(games):
    game = games[-1]
    game_participation = create_participation(
        game['game_id'],
        game['max_players'] + 5,
    )

    game_sessions = get_game_sessions(games, game_participation)
    expected_game_session = {
        'game_id': game['game_id'],
        'game_name': game['name'],
        'players': [
            player['user_id']
            for player in game_participation[:game['max_players']]
        ],
    }
    assert expected_game_session in game_sessions


def test_multiple_games_with_interest(games):
    game1 = games[0]
    game2 = games[1]
    game1_participation = create_participation(
        game1['game_id'],
        game1['min_players'],
    )
    game2_participation = create_participation(
        game2['game_id'],
        game2['min_players'],
        seed=game1['min_players'],
    )

    game_sessions = get_game_sessions(
        games,
        game1_participation + game2_participation,
    )
    expected_game_session1 = {
        'game_id': game1['game_id'],
        'game_name': game1['name'],
        'players': [
            player['user_id']
            for player in game1_participation[:game1['max_players']]
        ],
    }
    expected_game_session2 = {
        'game_id': game2['game_id'],
        'game_name': game2['name'],
        'players': [
            player['user_id']
            for player in game2_participation[:game2['max_players']]
        ],
    }
    assert expected_game_session1 in game_sessions
    assert expected_game_session2 in game_sessions


def generate_interest(num_players):
    return ['Player {}'.format(i) for i in range(num_players)]


def create_participation(game_id, num_players, seed=0):
    return [
        {
            'user_id': 'Player ID {}'.format(i),
            'name': 'Player Name {}'.format(i),
            'preferences': [game_id]
        } for i in range(seed, seed + num_players)
    ]
