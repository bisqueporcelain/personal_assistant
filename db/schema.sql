-- Conversational consistency for the semester assistant.
--
-- Two different jobs, deliberately separated:
--
--   conversations.sdk_session_id  lets the Claude Agent SDK resume its own
--                                 transcript, so the model keeps its context.
--   turns / continuity_notes      our own durable record, which survives a
--                                 session that cannot be resumed, compaction,
--                                 or a transcript pruned off disk.
--
-- The SDK transcript is authoritative for *what was said*. This database is
-- authoritative for *what must be remembered*. A row here is never a course
-- fact — those stay in courses/, outside version control and outside the
-- database, so staleness remains visible.

CREATE TABLE IF NOT EXISTS conversations (
    id              BIGSERIAL PRIMARY KEY,
    -- Stable handle the caller chooses: "default", or a course slug to keep
    -- one course's thread separate from another's.
    thread_key      TEXT        NOT NULL UNIQUE,
    -- The SDK session to resume. Null until the first turn completes, and
    -- rewritten on every turn: forking or compaction can change it.
    sdk_session_id  TEXT,
    title           TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_active_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS turns (
    id              BIGSERIAL   PRIMARY KEY,
    conversation_id BIGINT      NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    seq             INTEGER     NOT NULL,
    role            TEXT        NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    -- Which agent produced this: 'orchestrator', 'writer', 'scheduler', or
    -- NULL for the user's own turns.
    agent           TEXT,
    model           TEXT,
    -- Flattened text, for the continuity primer and for grepping.
    body            TEXT,
    -- Full content blocks, for reconstructing a turn exactly.
    blocks          JSONB,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (conversation_id, seq)
);

CREATE INDEX IF NOT EXISTS turns_conversation_seq_idx
    ON turns (conversation_id, seq DESC);

-- One row per completed assistant turn. Split from `turns` because it is
-- written later (the ResultMessage arrives after the text) and because nothing
-- reading the conversation back needs it.
CREATE TABLE IF NOT EXISTS turn_metrics (
    turn_id      BIGINT PRIMARY KEY REFERENCES turns(id) ON DELETE CASCADE,
    num_turns    INTEGER,
    duration_ms  INTEGER,
    cost_usd     NUMERIC(12, 6),
    stop_reason  TEXT,
    is_error     BOOLEAN NOT NULL DEFAULT FALSE,
    usage        JSONB
);

-- Facts about the *conversation* that must outlive the SDK transcript: a
-- decision reached, a preference stated, a correction the user made. Scoped so
-- a note about one course does not surface in another's thread.
--
-- Not a cache of course facts. If it belongs in courses/, it goes there.
CREATE TABLE IF NOT EXISTS continuity_notes (
    id              BIGSERIAL   PRIMARY KEY,
    conversation_id BIGINT      REFERENCES conversations(id) ON DELETE CASCADE,
    scope           TEXT        NOT NULL DEFAULT 'global',
    note            TEXT        NOT NULL,
    -- Where it came from: 'user' if stated outright, 'agent' if inferred.
    source          TEXT        NOT NULL DEFAULT 'agent',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    superseded_at   TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS continuity_notes_live_idx
    ON continuity_notes (conversation_id, scope, created_at DESC)
    WHERE superseded_at IS NULL;
