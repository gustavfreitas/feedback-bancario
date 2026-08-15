CREATE TABLE products_services (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(255)
);

CREATE TABLE channels (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(255)
);

CREATE TABLE manifestation_types (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(255)
);

CREATE TABLE manifestations (
    id                     SERIAL PRIMARY KEY,
    channel_id             INT NOT NULL REFERENCES channels(id) ON DELETE RESTRICT,
    manifestation_type_id  INT NOT NULL REFERENCES manifestation_types(id) ON DELETE RESTRICT,
    feedback_text          TEXT NOT NULL,
    satisfaction_score     SMALLINT CHECK (satisfaction_score BETWEEN 1 AND 5),
    sentiment              sentiment_level,
    urgency                urgency_level DEFAULT 'baixa',
    created_at             TIMESTAMP NOT NULL DEFAULT now(),
    updated_at             TIMESTAMP NOT NULL DEFAULT now()
);