DROP DATABASE IF EXISTS imdb_group_project;

CREATE DATABASE imdb_group_project;

USE imdb_group_project;

# A lot of writers / actors / director's don't have any information on their imdb page, 
# so I'm not sure what to do about that.


DROP TABLE IF EXISTS person;

CREATE TABLE person (
	person_id VARCHAR(7) PRIMARY KEY,
    person_name VARCHAR(256) NOT NULL,
    person_birthdate DATE 
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
    year_of_release INT NOT NULL,
	CONSTRAINT show_id_fk2
		FOREIGN KEY (show_id)
        REFERENCES tv_show (show_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


DROP TABLE IF EXISTS episode_person_relationship;

CREATE TABLE episode_person_relationship (
	episode_id VARCHAR(7) NOT NULL,
    person_id VARCHAR(7) NOT NULL,
    person_role ENUM('actor', 'writer', 'director'),
    CONSTRAINT episode_person_relationship_pk
		PRIMARY KEY (episode_id, person_id, person_role),
	CONSTRAINT episode_id_fk0
		FOREIGN KEY (episode_id)
        REFERENCES episode (episode_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
	CONSTRAINT person_id_fk0
		FOREIGN KEY (person_id)
        REFERENCES person (person_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


SELECT * FROM tv_show;

SELECT * FROM season;

SELECT * FROM episode;

SELECT * FROM person;




