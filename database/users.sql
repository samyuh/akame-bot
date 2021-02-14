PRAGMA foreign_keys = off;
.mode columns
.headers on
.nullvalue NULL

DROP TABLE IF EXISTS User;
CREATE TABLE User (
  idUser                    INTEGER                 PRIMARY KEY,
  name                      VARCHAR(255)            NOT NULL,
  color                     VARCHAR(255),
  connectTime               VARCHAR(255),
  lastTimeVoice             VARCHAR(255)
);
