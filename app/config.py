import os

DYNAMO_LOCAL_HOST = 'http://localhost:2345'
SESSION_TABLE_NAME = os.environ.get(
    'SESSION_TABLE',
    'MOCK_SESSION_TABLE_NAME',
)
