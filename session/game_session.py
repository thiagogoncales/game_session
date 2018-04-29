from collections import defaultdict


def get_game_sessions(games, participation):
    games_interest = defaultdict(list)
    for player_participation in participation:
        preference = player_participation['preferences']
        if not preference:
            continue
        games_interest[preference[0]].append(player_participation['user_id'])

    game_sessions = []
    for game in games:
        game_id = game['game_id']
        interest = games_interest[game_id]
        if game_has_enough_interest(game, interest):
            game_sessions.append({
                'game_id': game_id,
                'players': interest[:game['max_players']],
            })

    return game_sessions


def game_has_enough_interest(game, interest):
    return len(interest) >= game['min_players']
