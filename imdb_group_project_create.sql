DROP DATABASE IF EXISTS imdb_group_project;

CREATE DATABASE imdb_group_project;

USE imdb_group_project;


DROP TABLE IF EXISTS actor;

CREATE TABLE actor (
	actor_name VARCHAR(256) NOT NULL,
    actor_birthdate DATE NOT NULL,
    CONSTRAINT actor_pk
		PRIMARY KEY (actor_name, actor_birthdate)
);

DROP TABLE IF EXISTS director;

CREATE TABLE director (
	director_name VARCHAR(256) NOT NULL,
    director_birthdate DATE NOT NULL,
    CONSTRAINT director_pk
		PRIMARY KEY (director_name, director_birthdate)
);

DROP TABLE IF EXISTS writer;

CREATE TABLE writer (
	writer_name VARCHAR(256) NOT NULL,
    writer_birthdate DATE NOT NULL,
    CONSTRAINT writer_pk
		PRIMARY KEY (writer_name, writer_birthdate)
);


DROP TABLE IF EXISTS tv_show;

# Had to change the ID's to VARCHAR, since INT was deleting leading zeros
CREATE TABLE tv_show (
	show_id	VARCHAR(7) PRIMARY KEY,
	show_title VARCHAR(256) NOT NULL,
    show_score DECIMAL(2,1) NOT NULL,
    num_seasons INT NOT NULL,
    num_episodes INT NOT NULL,
    show_language VARCHAR(256) NOT NULL
);

DROP TABLE IF EXISTS season;

CREATE TABLE season (
	show_id VARCHAR(7) NOT NULL,
    season_num INT NOT NULL,
    num_episodes INT NOT NULL,
    CONSTRAINT season_pk
		PRIMARY KEY (show_id, season_num),
	CONSTRAINT show_id_fk1
		FOREIGN KEY (show_id)
        REFERENCES tv_show (show_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


DROP TABLE IF EXISTS episode;

CREATE TABLE episode (
	episode_id VARCHAR(7) PRIMARY KEY,
	show_id VARCHAR(7) NOT NULL,
    season_num INT NOT NULL,
    episode_num INT NOT NULL,
	episode_name VARCHAR(256),
    length INT NOT NULL,
    episode_score DECIMAL(2,1) NOT NULL,
    director_name VARCHAR(256) NOT NULL,
    air_date DATE NOT NULL,
	CONSTRAINT show_id_fk2
		FOREIGN KEY (show_id)
        REFERENCES tv_show (show_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
	CONSTRAINT director_name_fk
		FOREIGN KEY (director_name)
        REFERENCES director (director_name)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
		


DROP TABLE IF EXISTS episode_actor_relationship;

CREATE TABLE epoisode_actor_relationship (
	episode_id VARCHAR(7) NOT NULL,
    actor_name  VARCHAR(256) NOT NULL,
    CONSTRAINT episode_actor_relationship_pk
		PRIMARY KEY (episode_id, actor_name),
	CONSTRAINT episode_id_fk1
		FOREIGN KEY (episode_id)
        REFERENCES episode (episode_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
	CONSTRAINT actor_name_fk
		FOREIGN KEY (actor_name)
        REFERENCES actor (actor_name)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


DROP TABLE IF EXISTS episode_writer_relationship;

CREATE TABLE episode_writer_relationship (
	episode_id VARCHAR(7) NOT NULL,
    writer_name VARCHAR(256) NOT NULL,
    CONSTRAINT episode_writer_relationship_pk
		PRIMARY KEY (episode_id, writer_name),
	CONSTRAINT episode_id_fk2
		FOREIGN KEY (episode_id)
        REFERENCES episode (episode_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
	CONSTRAINT writer_name_fk
		FOREIGN KEY (writer_name)
        REFERENCES writer (writer_name)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


SELECT * FROM tv_show;




