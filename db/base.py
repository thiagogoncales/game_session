from pynamodb.models import Model

from config import DYNAMO_LOCAL_HOST


def set_host(cls):
    table_name = getattr(cls, 'table_name', '')
    if table_name.startswith('MOCK_'):
        setattr(cls, 'host', DYNAMO_LOCAL_HOST)
    setattr(cls, 'read_capacity_units', 1)
    setattr(cls, 'write_capacity_units', 1)
    setattr(cls, 'max_retry_attempts', 1)
    return cls


class BaseModel(Model):
    def as_dict(self):
        return {
            name: attr
            for name, attr in self.attribute_values.items()
        }
