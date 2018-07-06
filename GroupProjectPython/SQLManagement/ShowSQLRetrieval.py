# This file contains methods to retrieve data from the database
import mysql.connector

from SQLManagement import GenericRetrieval, SQLOperations


def get_top_rated_show_title():
    cnx = SQLOperations.get_connection()

    cursor = cnx.cursor()

    cursor.execute("SELECT get_top_rated_show_title()")

    for name in cursor:
        print(name[0])

    print('\n')

    cnx.close()


# Prints an array of strings of names of shows with the given actor in it
def get_shows_with_actor():
    actor_name = input("Enter the name of the actor to search for:\n")

    cnx = SQLOperations.get_connection()

    cursor = cnx.cursor()

    cursor.callproc('get_shows_with_actor', [actor_name])

    res = []

    for show in cursor.stored_results():
        res = show.fetchall()

    for r in res:
        print(r[0])

    print('\n')

    cnx.close()


# Prints an array of strings of show titles that had a ranking at or below the given number
def get_shows_of_top_given_number():
    try:
        num = int(input("Enter ranking of the shows you want to get:\n"))
    except ValueError:
        print("Invalid input")
        get_shows_of_top_given_number()
        return

    cnx = SQLOperations.get_connection()

    cursor = cnx.cursor()

    cursor.callproc('get_titles_of_top_given_number', [num])

    res = []

    for show in cursor.stored_results():
        res = show.fetchall()

    for r in res:
        print(r[0])

    print('\n')

    cnx.close()


# Prints the name of the show of the given rank
def get_show_of_rank():
    try:
        num = int(input("Enter the rank of the show you want to get:\n"))
    except ValueError:
        print("Invalid input")
        get_show_of_rank()
        return

    cnx = SQLOperations.get_connection()

    cursor = cnx.cursor()

    op = "SELECT get_show_of_rank(%d)" % num

    cursor.execute(op)

    for show in cursor:
        print(show[0])

    print('\n')

    cnx.close()


# Prints data about an episode with the given attributes
def get_episode_from_show():
    try:
        show_name = input("Enter the name of the show:\n")

        season_num = int(input("Enter the number of the season of the episode:\n"))

        episode_num = int(input("Enter the number of the episode:\n"))
    except ValueError:
        print("Invalid input")
        get_episode_from_show()
        return

    print()

    cnx = SQLOperations.get_connection()

    cursor = cnx.cursor()

    cursor.callproc('get_episode_from_show', [show_name, season_num, episode_num])

    res = []

    for show in cursor.stored_results():
        res = show.fetchall()

    for (episode_id, episode_name, length, episode_score, year_of_release) in res:
        print("ID: %s\nName: %s\nLength: %dmins\nScore: %1.1f\nYear of Release: %d\n"
              % (episode_id, episode_name, length, episode_score, year_of_release))

    if len(res) == 0:
        print("The given show %s does not exist in the database." % show_name)

    print()


def get_shows_with_number_of_seasons():
    try:
        num_seasons = int(input("Enter the number of seasons in the shows you want to look up:\n"))
    except ValueError:
        print("Invalid input")
        get_shows_with_number_of_seasons()
        return

    cnx = SQLOperations.get_connection()

    cursor = cnx.cursor()

    cursor.callproc('get_shows_with_number_of_seasons', [num_seasons])

    print("show_id\t\t\tshow_title")

    res = []

    for result in cursor.stored_results():
        res = result.fetchall()

    for r in res:
        print("%s\t\t\t%s" % (r[0], r[1]))

    print()


def main():
    action = input("What do you want to do:\n"
                   "retrieve data\n"
                   "get show of rank\n"
                   "get top rated show\n"
                   "get shows with actor\n"
                   "get shows of top rank\n"
                   "get number of roles\n"
                   "get episode from show\n"
                   "get shows with number of seasons\n"
                   "quit\n"
                   "\n")
    if action == "get show of rank":
        get_show_of_rank()
    elif action == "get top rated show":
        get_top_rated_show_title()
    elif action == "get shows with actor":
        get_shows_with_actor()
    elif action == "get shows of top rank":
        get_shows_of_top_given_number()
    elif action == "get number of roles":
        GenericRetrieval.get_number_of_roles()
    elif action == "get episode from show":
        get_episode_from_show()
    elif action == "retrieve data":
        GenericRetrieval.retrieve_info_from_table()
    elif action == "get shows with number of seasons":
        get_shows_with_number_of_seasons()
    elif action == "quit":
        exit(0)
    else:
        print("Invalid input\n")
        main()
        return


if __name__ == '__main__':
    main()
