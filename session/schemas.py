from voluptuous import (
    Required,
    Schema,
)


session_schema = Schema({
    Required('is_active'): bool,
})
