-- Postgres 9.1 or higher required.
CREATE TABLE IF NOT EXISTS :t (
    id int PRIMARY KEY,
    data bytea,
    mimetype varchar(255)
);
