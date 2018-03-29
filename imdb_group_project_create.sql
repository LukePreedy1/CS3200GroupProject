DROP DATABASE IF EXISTS imdb_group_project;

CREATE DATABASE imdb_group_project;

USE imdb_group_project;

# A lot of writers / actors / director's don't have any information on their imdb page, 
# so I'm not sure what to do about that.


DROP TABLE IF EXISTS actor;

CREATE TABLE actor (
	actor_id VARCHAR(7) PRIMARY KEY,
	actor_name VARCHAR(256) NOT NULL,
    actor_birthyear INT,
    actor_deathyear INT
);

DROP TABLE IF EXISTS director;

CREATE TABLE director (
	director_id VARCHAR(7) PRIMARY KEY,
	director_name VARCHAR(256) NOT NULL,
    director_birthyear INT,
    director_deathyear INT
);

DROP TABLE IF EXISTS writer;

CREATE TABLE writer (
	writer_id VARCHAR(7) PRIMARY KEY,
	writer_name VARCHAR(256) NOT NULL,
    writer_birthyear INT,
    writer_deathyear INT
);


DROP TABLE IF EXISTS tv_show;

# Had to change the ID's to VARCHAR, since INT was deleting leading zeros
CREATE TABLE tv_show (
	show_id	VARCHAR(7) PRIMARY KEY,
	show_title VARCHAR(256) NOT NULL,
    show_score DECIMAL(2,1) NOT NULL,
    num_seasons INT NOT NULL,
    num_episodes INT NOT NULL,
    show_language VARCHAR(256) NOT NULL,
    is_airing BOOLEAN NOT NULL
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
		


DROP TABLE IF EXISTS episode_actor_relationship;

CREATE TABLE epoisode_actor_relationship (
	episode_id VARCHAR(7) NOT NULL,
    actor_id  VARCHAR(7) NOT NULL,
    CONSTRAINT episode_actor_relationship_pk
		PRIMARY KEY (episode_id, actor_id),
	CONSTRAINT episode_id_fk1
		FOREIGN KEY (episode_id)
        REFERENCES episode (episode_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
	CONSTRAINT actor_id_fk
		FOREIGN KEY (actor_id)
        REFERENCES actor (actor_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


DROP TABLE IF EXISTS episode_writer_relationship;

CREATE TABLE episode_writer_relationship (
	episode_id VARCHAR(7) NOT NULL,
    writer_id VARCHAR(7) NOT NULL,
    CONSTRAINT episode_writer_relationship_pk
		PRIMARY KEY (episode_id, writer_id),
	CONSTRAINT episode_id_fk2
		FOREIGN KEY (episode_id)
        REFERENCES episode (episode_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
	CONSTRAINT writer_id_fk
		FOREIGN KEY (writer_id)
        REFERENCES writer (writer_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

DROP TABLE IF EXISTS episode_director_relationship;

CREATE TABLE episode_director_relationship (
	episode_id VARCHAR(7) NOT NULL,
    director_id VARCHAR(7) NOT NULL,
    CONSTRAINT episode_director_relationship_pk
		PRIMARY KEY (episode_id, director_id),
	CONSTRAINT episode_id_fk3
		FOREIGN KEY (episode_id)
        REFERENCES episode (episode_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
	CONSTRAINT director_id_fk
		FOREIGN KEY (director_id)
        REFERENCES director (director_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


SELECT * FROM tv_show;

SELECT * FROM season;

SELECT * FROM episode;




