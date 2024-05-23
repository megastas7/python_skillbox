CREATE TABLE IF NOT EXISTS 'actors' (
    act_id INTEGER PRIMARY KEY AUTOINCREMENT,
    act_first_name VARCHAR(50) NOT NULL,
    act_last_name VARCHAR(50) NOT NULL,
    act_gender VARCHAR(1) NOT NULL
);

CREATE TABLE IF NOT EXISTS 'movie' (
    mov_id INTEGER PRIMARY KEY AUTOINCREMENT,
    mov_title VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS 'director' (
    dir_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dir_first_name VARCHAR(50) NOT NULL,
    dir_last_name VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS 'movie_cast' (
  act_id INTEGER REFERENCES actors(act_id),
  mov_id INTEGER REFERENCES movie(mov_id),
  role VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS 'oscar_awarded' (
    award_id INTEGER PRIMARY KEY AUTOINCREMENT,
    mov_id INTEGER REFERENCES movie(mov_id)
);

CREATE TABLE IF NOT EXISTS 'movie_direction' (
    dir_id INTEGER REFERENCES director(dir_id),
    mov_id INTEGER REFERENCES movie(mov_id)
);
