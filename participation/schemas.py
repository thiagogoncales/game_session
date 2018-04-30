from voluptuous import (
    All,
    Length,
    Required,
    Schema,
)

participation_schema = Schema({
    Required('user_id'): All(str, Length(min=1)),
    Required('name'): All(str, Length(min=1)),
    Required('preferences'): list,
})
