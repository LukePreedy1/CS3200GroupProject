import mysql.connector


# Prints the number or roles the given actor has had in the database
from SQLManagement import MovieSQLRetrieval, ShowSQLRetrieval


def get_number_of_roles():
    actor_name = input("Enter the name of the actor you want to search for:\n")

    cnx = mysql.connector.connect(user='root',
                                  password='Yourface1234',
                                  host='127.0.0.1',
                                  database='imdb_solo_project')

    cursor = cnx.cursor()

    op = "SELECT get_number_of_roles('%s')" % actor_name

    cursor.execute(op)

    for num in cursor:
        print(num[0])

    print('\n')

    cnx.close()


def get_all_actor_roles():
    actor_name = input("Enter the name of the actor you want to search for:\n")

    cnx = mysql.connector.connect(user='root',
                                  passowrd='Yourface1234',
                                  host='127.0.0.1',
                                  database='imdb_solo_project')

    cursor = cnx.cursor()

    op1 = "SELECT get_shows_with_actor('%s')" % actor_name
    op2 = "SELECT get_movie_with_actor('%s')" % actor_name

    cursor.execute(op1)

    names = []

    for name in cursor:
        names.append(name[0])

    cursor.execute(op2)

    for name in cursor:
        names.append(name[0])

    for n in list(set(names)):
        print(n)

    print('\n')

    cnx.close()


# A generic retrieval method to retrieve data from the database
# Will be rather primitive, since its hard to make it better
def retrieve_info_from_table():
    cnx = mysql.connector.connect(user='root',
                                  password='Yourface1234',
                                  host='127.0.0.1',
                                  database='imdb_solo_project')

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


def main():
    while True:
        action = input("Which data type would you like to retrieve?\n"
                       "movies\n"
                       "shows\n"
                       "quit\n")

        if action == "movies":
            MovieSQLRetrieval.main()
        elif action == "shows":
            ShowSQLRetrieval.main()
        elif action == "quit":
            exit(0)
        else:
            print("Invalid input value, try again\n")


if __name__ == "__main__":
    main()
