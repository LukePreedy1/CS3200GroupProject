# This file contains methods to retrieve data from the database
import mysql.connector

from IMDbManagement.ShowAccessing import *


def get_top_rated_show_title():
    cnx = mysql.connector.connect(user='root',
                                  password='Yourface1234',
                                  host='127.0.0.1',
                                  database='imdb_group_project')

    cursor = cnx.cursor()

    cursor.execute("SELECT get_top_rated_show_title()")

    for name in cursor:
        print(name[0])

    print('\n')

    cnx.close()


# Prints an array of strings of names of shows with the given actor in it
def get_shows_with_actor():
    actor_name = input("Enter the name of the actor to search for:\n")

    cnx = mysql.connector.connect(user='root',
                                  password='Yourface1234',
                                  host='127.0.0.1',
                                  database='imdb_group_project')

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
    while True:
        try:
            num = int(input("Enter ranking of the shows you want to get:\n"))
            break
        except ValueError:
            print("Invalid input")


    cnx = mysql.connector.connect(user='root',
                                  password='Yourface1234',
                                  host='127.0.0.1',
                                  database='imdb_group_project')

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
    while True:
        try:
            num = int(input("Enter the rank of the show you want to get:\n"))
            break
        except ValueError:
            print("Invalid input")

    cnx = mysql.connector.connect(user='root',
                                  password='Yourface1234',
                                  host='127.0.0.1',
                                  database='imdb_group_project')

    cursor = cnx.cursor()

    op = "SELECT get_show_of_rank(%d)" % num

    cursor.execute(op)

    for show in cursor:
        print(show[0])

    print('\n')

    cnx.close()


# Prints the number or roles the given actor has had in the database
def get_number_of_roles():
    actor_name = input("Enter the name of the actor you want to search for:\n")

    cnx = mysql.connector.connect(user='root',
                                  password='Yourface1234',
                                  host='127.0.0.1',
                                  database='imdb_group_project')

    cursor = cnx.cursor()

    op = "SELECT get_number_of_roles('%s')" % actor_name

    cursor.execute(op)

    for num in cursor:
        print(num[0])

    print('\n')

    cnx.close()


# Prints data about an episode with the given attributes
def get_episode_from_show():
    while True:
        try:
            show_name = input("Enter the name of the show:\n")

            season_num = int(input("Enter the number of the season of the episode:\n"))

            episode_num = int(input("Enter the number of the episode:\n"))
            break

        except ValueError:
            print("Invalid input")

    print()

    cnx = mysql.connector.connect(user='root',
                                  password='Yourface1234',
                                  host='127.0.0.1',
                                  database='imdb_group_project')

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


# A generic retrieval method to retrieve data from the database
# Will be rather primitive, since its hard to make it better
def retrieve_info_from_table():
    cnx = mysql.connector.connect(user='root',
                                  password='Yourface1234',
                                  host='127.0.0.1',
                                  database='imdb_group_project')

    cursor = cnx.cursor()

    query = "SHOW TABLES"
    cursor.execute(query)

    print("Enter the name of the table you want to retrieve from:")

    tables = []

    for t in cursor:
        tables.append(t[0])
        print(t[0])

    table = input()

    while table not in tables:
        table = input("Please enter a valid table name:\n")

    query = "SHOW COLUMNS FROM %s" % table
    cursor.execute(query)

    print("Enter the name of the column(s) from the table you selected:")
    print("For multiple columns, enter multiple names on a single line separated by a space")

    columns = []

    for c in cursor:
        columns.append(c[0])
        print(c[0] + '\t' + c[1])

    col = input()
    col = col.split(' ')

    # Checks that all the names given are valid
    while True:
        safe = True
        for c in col:
            if c in columns:
                safe = safe and True
            else:
                safe = False
        if safe:
            break
        elif len(col) == 1 and col[0] == "*":
            col = columns
            break
        else:
            col = input("Please enter only valid column names:\n")
            col = col.split(' ')

    while True:
        s = input("Do you want to sort (y/n):\n")
        if s == "y":
            sorting = True
            break
        elif s == "n":
            sorting = False
            break
        else:
            print("Invalid input")

    if sorting:
        while True:
            print("Column to sort by:")
            for c in col:
                print(c)

            sort_by = input()

            if sort_by in col:
                break
            else:
                print("Enter valid column name")

        while True:
            a = input("Ascending or descending (a/d):")

            if a == "a":
                asc = True
                break
            elif a == "d":
                asc = False
                break
            else:
                print("Invalid input")

    while True:
        g = input("Do you want to group by a column (y/n):\n")

        if g == "y":
            grouping = True
            break
        elif g == "n":
            grouping = False
            break
        else:
            print("Invalid input")

    if grouping:
        while True:
            print("Choose a column to group by:")
            for c in col:
                print(c)

            group_by = input()

            if group_by in col:
                break
            else:
                print("Invalid input")

    while True:
        will_limit = input("Do you want to limit the results (y/n):\n")

        if will_limit == "y":
            limiting = True
            break
        elif will_limit == "n":
            limiting = False
            break
        else:
            print("Invalid input")

    if limiting:
        while True:
            try:
                limit_by = int(input("Enter number to limit by:\n"))
                break
            except ValueError:
                print("Invalid input")

    query = "SELECT "

    for c in col:
        query += c + ", "

    query = query[:-2]
    query += " FROM %s" % table

    if grouping:
        query += " GROUP BY %s" % group_by

    if sorting:
        query += " ORDER BY %s" % sort_by
        if asc:
            query += " ASC"
        else:
            query += " DESC"

    if limiting:
        query += " LIMIT %d" % limit_by

    cursor.execute(query)

    for res in cursor:
        result = ""

        for r in res:
            result += str(r) + " "

        print(result)


def get_shows_with_number_of_seasons():
    while True:
        try:
            num_seasons = int(input("Enter the number of seasons in the shows you want to look up:\n"))
            break
        except ValueError:
            print("Invalid input")

    cnx = mysql.connector.connect(user='root',
                                  password='Yourface1234',
                                  host='127.0.0.1',
                                  database='imdb_group_project')

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
    while True:
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
            get_number_of_roles()
        elif action == "get episode from show":
            get_episode_from_show()
        elif action == "retrieve data":
            retrieve_info_from_table()
        elif action == "get shows with number of seasons":
            get_shows_with_number_of_seasons()
        elif action == "quit":
            exit(0)
        else:
            print("Invalid input\n")


if __name__ == '__main__':
    main()
