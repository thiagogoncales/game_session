import pytest

from session.game_session import (
    game_has_enough_interest,
    organize_game_session,
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


def test_organize_game_session_enough_players(games):
    game = games[-1]
    game_participation = create_participation(
        game['game_id'],
        game['min_players'],
    )

    game_session = organize_game_session(games, game_participation)
    assert game_session[game['game_id']]['players'] == [
        player['user_id']
        for player in game_participation
    ]

def test_organize_game_session_not_enough_players(games):
    game = games[-1]
    game_participation = create_participation(
        game['game_id'],
        game['min_players'] - 1,
    )

    game_session = organize_game_session(games, game_participation)
    assert game['game_id'] not in game_session


def test_organize_game_session_too_many_players(games):
    game = games[-1]
    game_participation = create_participation(
        game['game_id'],
        game['max_players'] + 5,
    )

    game_session = organize_game_session(games, game_participation)
    assert game_session[game['game_id']]['players'] == [
        player['user_id']
        for player in game_participation[:game['max_players']]
    ]


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

    game_session = organize_game_session(
        games,
        game1_participation + game2_participation,
    )
    assert game_session[game1['game_id']]['players'] == [
        player['user_id']
        for player in game1_participation[:game1['max_players']]
    ]
    assert game_session[game2['game_id']]['players'] == [
        player['user_id']
        for player in game2_participation[:game2['max_players']]
    ]



def generate_interest(num_players):
    return ['Player {}'.format(i) for i in range(num_players)]


def create_participation(game_id, num_players, seed=0):
    return [
        {
            'user_id': 'Player ID {}'.format(i),
            'name': 'Player Name {}'.format(i),
            'preference': [game_id]
        } for i in range(seed, seed + num_players)
    ]
