CREATE TABLE IF NOT EXISTS posts (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    karma INT NOT NULL,
    num_comments INT NOT NULL
);

CREATE TABLE IF NOT EXISTS comments (
    id TEXT PRIMARY KEY,
    post_id TEXT REFERENCES posts(id) ON DELETE CASCADE NOT NULL,
    body TEXT NOT NULL,
    karma INT NOT NULL
);