DROP TABLE IF EXISTS post_joins;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS users;

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR NOT NULL UNIQUE,
    password_hash VARCHAR NOT NULL
);

CREATE TABLE posts (
    post_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id),
    post TEXT NOT NULL,
    needed INTEGER,
    joined INTEGER DEFAULT 0
);

CREATE TABLE post_joins (
    join_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(user_id),
    post_id UUID NOT NULL REFERENCES posts(post_id)
);