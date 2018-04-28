import os

DYNAMO_LOCAL_HOST = 'http://localhost:2345'

SESSION_TABLE_NAME = os.environ.get(
    'SESSION_TABLE_NAME',
    'MOCK_SESSION_TABLE_NAME',
)
GAME_TABLE_NAME = os.environ.get(
    'GAME_TABLE_NAME',
    'MOCK_GAME_TABLE_NAME',
)
