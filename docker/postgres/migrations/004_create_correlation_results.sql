BEGIN;

CREATE TABLE IF NOT EXISTS correlation_results (

    correlation_id BIGSERIAL PRIMARY KEY,

    session_id VARCHAR(100) NOT NULL,

    rule_id VARCHAR(50) NOT NULL,

    rule_name VARCHAR(150) NOT NULL,

    severity VARCHAR(30) NOT NULL,

    score DOUBLE PRECISION NOT NULL,

    threat_type VARCHAR(100) NOT NULL,

    description TEXT NOT NULL,

    evidence JSONB NOT NULL DEFAULT '{}'::jsonb,

    model_name VARCHAR(100) NOT NULL,

    model_version VARCHAR(50) NOT NULL,

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_correlation_session
        FOREIGN KEY (session_id)
        REFERENCES sessions(session_id)
        ON DELETE CASCADE,

    CONSTRAINT chk_correlation_score
        CHECK (
            score >= 0
            AND score <= 1
        ),

    CONSTRAINT uq_correlation_result
        UNIQUE (
            session_id,
            rule_id,
            model_name,
            model_version
        )
);


CREATE INDEX IF NOT EXISTS
    idx_correlation_session
ON correlation_results(session_id);


CREATE INDEX IF NOT EXISTS
    idx_correlation_rule
ON correlation_results(rule_id);


CREATE INDEX IF NOT EXISTS
    idx_correlation_threat
ON correlation_results(threat_type);


CREATE INDEX IF NOT EXISTS
    idx_correlation_severity
ON correlation_results(severity);


COMMIT;
