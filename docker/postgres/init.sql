CREATE TABLE IF NOT EXISTS normalized_events (

    event_id UUID PRIMARY KEY,

    schema_version VARCHAR(10) NOT NULL,

    source VARCHAR(50) NOT NULL,

    event_type VARCHAR(100) NOT NULL,

    rule_id VARCHAR(100),

    rule_name VARCHAR(255),

    mitre_technique VARCHAR(100),

    event_timestamp TIMESTAMP NOT NULL,

    ingest_timestamp TIMESTAMP NOT NULL,

    session_id VARCHAR(100),

    native_uid VARCHAR(100),

    severity INTEGER,

    severity_native VARCHAR(50),

    label VARCHAR(100),

    network JSONB,

    host JSONB,

    enrichment JSONB,

    data JSONB,

    raw_log JSONB

);