from pynamodb.attributes import (
    JSONAttribute,
    UnicodeAttribute,
)

from db.base import (
    set_host,
    BaseModel,
)
from config import (
    PARTICIPATION_TABLE_NAME,
)

class Participation(BaseModel):
    session_id = UnicodeAttribute(hash_key=True)
    user_id = UnicodeAttribute(range_key=True)
    name = UnicodeAttribute()
    preferences = JSONAttribute()

    @set_host
    class Meta:
        table_name = PARTICIPATION_TABLE_NAME
