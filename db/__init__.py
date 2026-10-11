"""Conversation persistence.

The schema is tracked (`schema.sql`); the data it holds is not. Nothing in here
stores a course fact — those stay in `courses/`, where their staleness is
visible. This stores what was *said*, so a new session can pick up where the
last one stopped.
"""

from .store import (
    DEFAULT_DSN,
    DSN_ENV_VAR,
    SCHEMA_PATH,
    ConversationStore,
    NullStore,
    PostgresStore,
    Thread,
    configured_dsn,
    open_store,
)

__all__ = [
    "DEFAULT_DSN",
    "DSN_ENV_VAR",
    "SCHEMA_PATH",
    "ConversationStore",
    "NullStore",
    "PostgresStore",
    "Thread",
    "configured_dsn",
    "open_store",
]
