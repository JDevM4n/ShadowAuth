BEGIN;

CREATE TABLE IF NOT EXISTS sessions (

    session_id VARCHAR(100) PRIMARY KEY,

    sources TEXT[] NOT NULL DEFAULT '{}',

    first_event_timestamp TIMESTAMPTZ NOT NULL,

    last_event_timestamp TIMESTAMPTZ NOT NULL,

    event_count INTEGER NOT NULL DEFAULT 0,

    label VARCHAR(30) NOT NULL DEFAULT 'unlabeled',

    attack_type VARCHAR(50),

    label_source VARCHAR(50),

    label_confidence NUMERIC(5,4),

    labeled_at TIMESTAMPTZ,

    data_origin VARCHAR(30) NOT NULL DEFAULT 'unknown',

    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_sessions_label
        CHECK (
            label IN (
                'attack',
                'benign',
                'unlabeled'
            )
        ),

    CONSTRAINT chk_sessions_confidence
        CHECK (
            label_confidence IS NULL
            OR (
                label_confidence >= 0
                AND label_confidence <= 1
            )
        )
);


CREATE INDEX IF NOT EXISTS idx_sessions_label
    ON sessions(label);


CREATE INDEX IF NOT EXISTS idx_sessions_first_event
    ON sessions(first_event_timestamp);


CREATE INDEX IF NOT EXISTS idx_normalized_events_session
    ON normalized_events(session_id);


INSERT INTO sessions (

    session_id,

    sources,

    first_event_timestamp,

    last_event_timestamp,

    event_count,

    label,

    label_source,

    label_confidence,

    labeled_at,

    data_origin

)

SELECT

    session_id,

    ARRAY_AGG(DISTINCT source),

    MIN(event_timestamp),

    MAX(event_timestamp),

    COUNT(*),

    CASE

        WHEN BOOL_OR(label = 'attack')
            THEN 'attack'

        WHEN BOOL_OR(label = 'benign')
            THEN 'benign'

        ELSE 'unlabeled'

    END,

    CASE

        WHEN BOOL_OR(label = 'attack')
            OR BOOL_OR(label = 'benign')
            THEN 'analyst_review'

        ELSE NULL

    END,

    CASE

        WHEN BOOL_OR(label = 'attack')
            OR BOOL_OR(label = 'benign')
            THEN 1.0

        ELSE NULL

    END,

    CASE

        WHEN BOOL_OR(label = 'attack')
            OR BOOL_OR(label = 'benign')
            THEN CURRENT_TIMESTAMP

        ELSE NULL

    END,

    CASE

        WHEN session_id = '7954f7782c6f'
            THEN 'controlled'

        ELSE 'live'

    END

FROM normalized_events

WHERE session_id IS NOT NULL

GROUP BY session_id

ON CONFLICT (session_id) DO NOTHING;


UPDATE sessions

SET
    label_source = 'controlled_attack',
    label_confidence = 1.0,
    data_origin = 'controlled',
    updated_at = CURRENT_TIMESTAMP

WHERE session_id = '7954f7782c6f';


COMMIT;
