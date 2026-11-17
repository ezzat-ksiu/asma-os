-- ASMA-OS initial PostgreSQL schema
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS audit_ledger (
    entry_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    occurred_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    actor TEXT NOT NULL,
    action TEXT NOT NULL,
    details JSONB NOT NULL DEFAULT '{}'::jsonb
);
CREATE INDEX IF NOT EXISTS audit_ledger_occurred_at_idx ON audit_ledger (occurred_at DESC);

CREATE TABLE IF NOT EXISTS mesh_nodes (
    node_id TEXT PRIMARY KEY,
    node_type TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'initializing',
    health_score DOUBLE PRECISION NOT NULL DEFAULT 1.0 CHECK (health_score BETWEEN 0 AND 1),
    capabilities JSONB NOT NULL DEFAULT '[]'::jsonb,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS operational_gates (
    gate_id TEXT PRIMARY KEY CHECK (gate_id ~ '^G[0-6]$'),
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    criteria JSONB NOT NULL DEFAULT '[]'::jsonb,
    status TEXT NOT NULL DEFAULT 'PENDING'
        CHECK (status IN ('PENDING', 'IN_PROGRESS', 'PASSED', 'FAILED')),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS workflow_state_checkpoints (
    checkpoint_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_id TEXT NOT NULL,
    state JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (workflow_id, checkpoint_id)
);
CREATE INDEX IF NOT EXISTS workflow_checkpoints_latest_idx
    ON workflow_state_checkpoints (workflow_id, created_at DESC);
