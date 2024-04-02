CREATE SCHEMA IF NOT EXISTS showcase;

CREATE TABLE showcase.counters (
    counter_id integer  NOT NULL,
    value integer NOT NULL,
    CONSTRAINT pk_counters PRIMARY KEY ( counter_id )
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

INSERT INTO showcase.counters VALUES (1,0), (2,0);