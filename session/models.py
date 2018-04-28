from pynamodb.attributes import (
    BooleanAttribute,
    UnicodeAttribute,
)
from pynamodb.models import Model

from db.base import (
    set_host,
    BaseModel,
)
from config import (
    SESSION_TABLE_NAME,
)


class Session(BaseModel):
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
