BEGIN;

CREATE TABLE IF NOT EXISTS incidents (
    incident_id BIGSERIAL PRIMARY KEY,

    correlation_id BIGINT UNIQUE,

    session_id VARCHAR(100) NOT NULL,

    title VARCHAR(255) NOT NULL,

    description TEXT,

    threat_type VARCHAR(100),

    severity VARCHAR(30) NOT NULL DEFAULT 'medium',

    status VARCHAR(30) NOT NULL DEFAULT 'open',

    evidence JSONB NOT NULL DEFAULT '{}'::jsonb,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    resolved_at TIMESTAMPTZ,

    CONSTRAINT chk_incident_status
        CHECK (
            status IN (
                'open',
                'investigating',
                'resolved'
            )
        ),

    CONSTRAINT chk_incident_severity
        CHECK (
            severity IN (
                'low',
                'medium',
                'high',
                'critical'
            )
        )
);

CREATE INDEX IF NOT EXISTS idx_incidents_status
    ON incidents(status);

CREATE INDEX IF NOT EXISTS idx_incidents_session
    ON incidents(session_id);

CREATE INDEX IF NOT EXISTS idx_incidents_threat
    ON incidents(threat_type);

COMMIT;
