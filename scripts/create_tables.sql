CREATE TYPE classification_type AS ENUM (
    'travel_tip',
    'travel_suggestion',
    'other'
);

CREATE TABLE IF NOT EXISTS posts (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    score INT NOT NULL
);

CREATE TABLE IF NOT EXISTS comments (
    id TEXT PRIMARY KEY,
    post_id TEXT REFERENCES posts(id) ON DELETE CASCADE NOT NULL,
    body TEXT NOT NULL,
    score INT NOT NULL,
    classification classification_type NOT NULL,
    start_date DATE,
    end_date DATE
);

CREATE TABLE IF NOT EXISTS locations (
    id SERIAL PRIMARY KEY,
    comment_id TEXT REFERENCES comments(id) ON DELETE CASCADE NOT NULL,
    lat DOUBLE PRECISION,
    lng DOUBLE PRECISION
);
