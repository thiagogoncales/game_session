from voluptuous import (
    All,
    Invalid,
    Length,
    Range,
    Required,
    Schema,
)


def min_players_must_be_less_than_max_players(data):
    if data['min_players'] >= data['max_players']:
        raise Invalid('min_players must be less than max_players')
    return data


game_schema = Schema(All({
    Required('name'): All(str, Length(min=1)),
    Required('min_players'): All(int, Range(min=1)),
    Required('max_players'): All(int, Range(min=1)),
}, min_players_must_be_less_than_max_players))
