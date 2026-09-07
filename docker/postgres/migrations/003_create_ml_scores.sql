CREATE TABLE IF NOT EXISTS ml_scores (

    score_id BIGSERIAL PRIMARY KEY,

    session_id TEXT NOT NULL,

    model_name TEXT NOT NULL,

    model_version TEXT NOT NULL,

    prediction TEXT NOT NULL,

    attack_probability DOUBLE PRECISION,

    anomaly_score DOUBLE PRECISION,

    artifact_path TEXT,

    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_ml_scores_session
        FOREIGN KEY (session_id)
        REFERENCES sessions(session_id)
        ON DELETE CASCADE,

    CONSTRAINT ck_ml_attack_probability
        CHECK (
            attack_probability IS NULL
            OR (
                attack_probability >= 0
                AND attack_probability <= 1
            )
        ),

    CONSTRAINT uq_ml_session_model
        UNIQUE (
            session_id,
            model_name,
            model_version
        )
);


CREATE INDEX IF NOT EXISTS idx_ml_scores_session_id
    ON ml_scores(session_id);


CREATE INDEX IF NOT EXISTS idx_ml_scores_prediction
    ON ml_scores(prediction);


CREATE INDEX IF NOT EXISTS idx_ml_scores_attack_probability
    ON ml_scores(attack_probability);
