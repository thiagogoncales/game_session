from pynamodb.attributes import (
    BooleanAttribute,
    UnicodeAttribute,
)
from pynamodb.models import Model

from config import (
    DYNAMO_LOCAL_HOST,
    SESSION_TABLE_NAME,
)


def set_host(cls):
    table_name = getattr(cls, 'table_name', '')
    if table_name.startswith('MOCK_'):
        setattr(cls, 'host', DYNAMO_LOCAL_HOST)
    setattr(cls, 'read_capacity_units', 1)
    setattr(cls, 'write_capacity_units', 1)
    setattr(cls, 'max_retry_attempts', 1)
    return cls


class Session(Model):
    session_id = UnicodeAttribute(hash_key=True)
    is_active = BooleanAttribute()

    def as_dict(self):
        return {
            name: attr
            for name, attr in self.attribute_values.items()
        }

    @set_host
    class Meta:
        table_name = SESSION_TABLE_NAME

