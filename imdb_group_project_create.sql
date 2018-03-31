DROP DATABASE IF EXISTS imdb_group_project;

CREATE DATABASE imdb_group_project;

USE imdb_group_project;

# Since it is taking forever to run the program, I've simplified the data.
# Now, it will only track the first 5 actors found on IMDb, making this data much 
# easier to test and work with.


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
    show_language VARCHAR(256) NOT NULL,
    show_rank INT UNIQUE NOT NULL
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


DROP PROCEDURE IF EXISTS get_titles_of_top_given_number;

DELIMITER //

# Gets the titles and ranks of all shows with a rank below the given amount
CREATE PROCEDURE get_titles_of_top_given_number(IN num INT)
BEGIN
	SELECT show_title, show_rank FROM tv_show 
		WHERE show_rank <= num
        ORDER BY show_rank;
END//

DELIMITER ;

DROP FUNCTION IF EXISTS get_top_rated_show_title;

DELIMITER //

# Returns the title of the top rated show
CREATE FUNCTION get_top_rated_show_title()
	RETURNS VARCHAR(256)
BEGIN
	DECLARE ret VARCHAR(256);
    
    SELECT show_title INTO ret FROM tv_show
		WHERE show_rank = 1;
        
	RETURN ret;
END//

DELIMITER ;

DROP PROCEDURE IF EXISTS get_shows_with_director;

DELIMITER //

# Gets the set of show titles that have an actor 
# with the given name in any of their episodes.
CREATE PROCEDURE get_shows_with_actor(IN actor_name VARCHAR(256))
BEGIN
	SELECT show_title FROM tv_show JOIN
		episode ON (episode.show_id = tv_show.show_id) JOIN
        episode_person_relationship ON 
			(episode_person_relationship.episode_id = episode.episode_id) AND
			(person_role = 'actor') JOIN
		person ON (person.person_id = episode_person_relationship.person_id)
		WHERE person_name = actor_name;
END//

DELIMITER ;


SELECT * FROM tv_show;

SELECT * FROM season;

SELECT * FROM episode;

SELECT * FROM person;




