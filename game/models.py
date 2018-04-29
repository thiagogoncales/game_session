from pynamodb.attributes import (
    NumberAttribute,
    UnicodeAttribute,
)

from db.base import (
    set_host,
    BaseModel,
)
from config import (
    GAME_TABLE_NAME,
)


class Game(BaseModel):
    session_id = UnicodeAttribute(hash_key=True)
    game_id = UnicodeAttribute(range_key=True)
    name = UnicodeAttribute()
    min_players = NumberAttribute()
    max_players = NumberAttribute()

    @set_host
    class Meta:
        table_name = GAME_TABLE_NAME
