import os

DYNAMO_LOCAL_HOST = 'http://localhost:2345'


def _get_table_name(table_name):
    return os.environ.get(
        table_name,
        'MOCK_{}'.format(table_name),
    )

SESSION_TABLE_NAME = _get_table_name('SESSION_TABLE_NAME')
GAME_TABLE_NAME = _get_table_name('GAME_TABLE_NAME')
PARTICIPATION_TABLE_NAME = _get_table_name('PARTICIPATION_TABLE_NAME')
