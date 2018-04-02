from IMDbStuff.Accessing import *

import mysql.connector

from SQLManagement import SQLRetrieval


# Does the given operation to the database
def perform_operation_on_db(op):
    cnx = mysql.connector.connect(user='root',
                                  password='Yourface1234',
                                  host='127.0.0.1',
                                  database='imdb_group_project')

    cursor = cnx.cursor()

    try:
        cursor.execute(op)
        cnx.commit()
        cnx.close()
    except mysql.connector.Error as err:
        print("Could not perform the given operation")
        print(err.msg)
        exit(1)


# Gets the title of the show as a string, adds the show to the database.  does not return
def add_show_from_id(id, rank):
    ia = imdb.IMDb()

    show = ia.get_movie(id)

    # CANNOT ACCESS PRODUCTION COMPANY, NEED TO REMOVE!
    add_show = ("INSERT INTO tv_show "
                "(show_id, show_title, show_score, num_seasons, num_episodes, show_language, show_rank) "
                "VALUES (%s, %s, %1.1f, %d, %d, %s, %d)")

    # Need to call this before checking data.  Still not sure why, but it's important.
    ia.update(show, 'episodes')

    # When inserting strings, they must be in quotes, otherwise it throws an error.
    show_title = "\"" + show['title'] + "\""

    # Some shows don't have a listed language (Looking at you Ash vs. Evil Dead), so I'm just calling it "unlisted"
    try:
        show_language = "\"" + show['lang'][0] + "\""
    except KeyError as ke:
        print("Failed on language for show: ")
        print(show_title)
        print("Will just set it to unlisted and just pretend.")
        show_language = "\"unlisted\""

    show_id = "\"" + show.movieID + "\""

    # I'm doing a lot of checking for edge cases.  For some reason, Naruto: Shippûden at rank 237, despite having
    # 505 episodes, does not have any seasons.  To account for that, if a show does not have any seasons, it will
    # set it to 0, and just pretend that it makes sense.
    try:
        num_seasons = int(show['seasons'])
    except KeyError as ke:
        print("This show does not have any seasons.  Setting to 0 as a default.")
        num_seasons = 0

    # Chose not to make the movieID an int, since that would get rid of leading 0's
    show_result = add_show % (show_id,
                              show_title,
                              float(show['rating']),
                              num_seasons,
                              int(show['number of episodes']),
                              show_language,
                              rank)

    # Performs the given code on the database
    perform_operation_on_db(show_result)

    # A special edge case for when the show is listed as having 0 seasons
    if num_seasons == 0:
        add_season = ("INSERT INTO season "
                      "(show_id, season_num, num_episodes) "
                      "VALUES (%s, %d, %d)")

        season_result = add_season % (show_id,
                                      0,
                                      len(show['episodes']['unknown season']))

        perform_operation_on_db(season_result)

        for ep in range(0, len(show['episodes']['unknown season'])):
            try:
                add_episode_to_database(show['episodes']['unknown season'][ep], show_id)
            except KeyError as ke:
                print("Show %s does not have an episode %d in season %d" % (show_title, ep, 0))

    # Will add all the seasons to the database
    for i in range(1, show['seasons']+1):
        add_season = ("INSERT INTO season "
                      "(show_id, season_num, num_episodes) " 
                      "VALUES (%s, %d, %d)")

        try:
            season_result = add_season % (show_id,
                                          i,
                                          len(show['episodes'][i]))

            perform_operation_on_db(season_result)
        except KeyError as ke:
            # For some reason, Dragonball Z at rank 74 does not have a season 2, but does have seasons 3 and 4,
            # and that's making the program angry.
            # I'm just going to ignore it.  It's not my fault somebody at IMDb made a mistake.
            print("Show %s season %d had an error" % (show_title, i))
            continue

        # For each episode in that season, add its information to the database
        # Some shows have an episode 0, and can only be found with that.  Will use a try
        # except to make sure that it will be caught, and doesn't cause any errors.
        for j in range(0, len(show['episodes'][i]) + 1):
            try:
                e = show['episodes'][i][j]
                ia.update(e)
                add_episode_to_database(e, show_id, ia)
            except KeyError as ke:
                continue

        print("Added show %s to the database" % show_title)


# Given an episode object, will add the data in the episode to the database.
def add_episode_to_database(episode, show_id, ia):
    add_episode = ("INSERT INTO episode "
                   "(episode_id, show_id, season_num, episode_num, episode_name, length, "
                   "episode_score, year_of_release) "
                   "VALUES (%s, %s, %d, %d, %s, %d, %1.1f, %d)")

    episode_id = "\"" + episode.movieID + "\""

    episode_title = "\"" + episode['title'] + "\""

    episode_result = add_episode % (episode_id,
                                    show_id,
                                    int(episode['season']),
                                    int(episode['episode']),
                                    episode_title,
                                    int(episode['runtime'][0]),
                                    float(episode['rating']),
                                    int(episode['year']))

    perform_operation_on_db(episode_result)

    try:
        directors = episode['director']
    except KeyError as ke:
        directors = []

    try:
        writers = episode['writer']
    except KeyError as ke:
        writers = []

    try:
        actors = episode['cast']
    except KeyError as ke:
        actors = []

    # It's taking a long time to add shows with many actors and writers, so to make it easier,
    # I'm only going to add 5 actors from each episode.

    # A lot of time is wasted trying to add the same person many times, so I'm trying to fix that.  Will query the
    # database (which is faster than checking IMDb, for each person) then if it is not there, will add the person.
    for d in directors:
        add_relationship_to_database(get_person_id(d), episode_id, "'director'")
        if check_if_database_has_person(d.personID):
            continue
        ia.update(d)
        add_person_to_database(d)

    for w in writers:
        add_relationship_to_database(get_person_id(w), episode_id, "'writer'")
        if check_if_database_has_person(w.personID):
            continue
        ia.update(w)
        add_person_to_database(w)

    num_actors = 0
    for a in actors:
        if num_actors == 5:
            break
        add_relationship_to_database(get_person_id(a), episode_id, "'actor'")
        if check_if_database_has_person(a.personID):
            continue
        ia.update(a)
        add_person_to_database(a)
        num_actors += 1

    print("Added episode %s to the database" % episode_title)


def get_person_id(p):
    return "\"" + p.personID + "\""


# Returns a boolean based on if the database contains the given person id
def check_if_database_has_person(id):
    cnx1 = mysql.connector.connect(user='root',
                                   password='Yourface1234',
                                   host='127.0.0.1',
                                   database='imdb_group_project')

    cursor = cnx1.cursor()

    query = "SELECT person_id FROM person WHERE person_id = %s" % id

    cursor.execute(query)

    for person_id in cursor:
        cnx1.close()
        return True

    cnx1.close()
    return False


# adds the given director of the given episode to the database.
def add_person_to_database(p):
    # The IGNORE is there so that the same person won't be inserted twice.
    add_person = "INSERT IGNORE INTO person (person_id, person_name"

    person_id = "\"" + p.personID + "\""

    person_name = "\"" + p['name'] + "\""

    # only include the birthdate if IMDb has one listed
    if p.get('birth date') is None:
        add_person += ") VALUES (%s, %s)"
        person_results = add_person % (person_id, person_name)
    else:
        add_person += ", person_birthdate) VALUES (%s, %s, '%s')"
        person_results = add_person % (person_id, person_name, p.get('birth date'))

    perform_operation_on_db(person_results)

    print("Added person %s to the database" % person_name)


def add_relationship_to_database(p_id, e_id, role):
    # The IGNORE is there so if a person has multiple roles, they won't be added badly.
    add_relationship = ("INSERT IGNORE INTO episode_person_relationship "
                        "(episode_id, person_id, person_role) "
                        "VALUES (%s, %s, %s)")

    relationship_results = add_relationship % (e_id, p_id, role)
    perform_operation_on_db(relationship_results)


# Initializes the database with the given data
def initialize_database():
    reset_database()

    # Will loop until given valid input
    while True:
        num = int(input("Enter how many shows you want to retrieve, up to 250:\n"))
        if 0 < int(num) <= 250:
            break

    ids = get_top_number(num)

    for i in range(0, len(ids)):
        add_show_from_id(ids[i], i + 1)


# Resets the database data
def reset_database():
    cnx2 = mysql.connector.connect(user='root',
                                   password='Yourface1234',
                                   host='127.0.0.1',
                                   database='imdb_group_project')

    cursor = cnx2.cursor()

    cursor.execute("CALL reset_database()")

    cnx2.close()


# The Main method that will be run to make everything do what it's supposed to do
def main():
    # Will loop until given valid input
    while True:
        action = input("What do you want to do:\n"
                       "initialize database\n"
                       "reset database\n"
                       "retrieve data\n"
                       "quit\n"
                       "\n")
        if action == "initialize database":
            initialize_database()
            break
        elif action == "retrieve data":
            SQLRetrieval.main()
            break
        elif action == "reset database":
            reset_database()
            break
        elif action == "quit":
            exit(0)
        else:
            print("Invalid action")

    exit(0)


if __name__ == "__main__":
    main()
