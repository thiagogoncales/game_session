from collections import defaultdict


def organize_game_session(games, participation):
    games_interest = defaultdict(list)
    for player_participation in participation:
        preference = player_participation['preference']
        if not preference:
            continue
        games_interest[preference[0]].append(player_participation['user_id'])

    games_session = {}
    for game in games:
        game_id = game['game_id']
        interest = games_interest[game_id]
        if game_has_enough_interest(game, interest):
            games_session[game_id] = {
                'game_name': game['name'],
                'players': interest[:game['max_players']],
            }

    return games_session


def game_has_enough_interest(game, interest):
    return len(interest) >= game['min_players']
