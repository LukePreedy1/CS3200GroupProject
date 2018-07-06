from SQLManagement import GenericRetrieval, SQLOperations


def get_movie_of_rank():
    try:
        rank = int(input("Enter the number of the rank you want:\n"))
    except ValueError:
        print("Please enter an integer.\n")
        get_movie_of_rank()
        return

    if rank <= 0:
        print("Given rank must be >= 0\n")
        get_movie_of_rank()
        return

    get_movie_of_rank_given(rank)


def get_movie_of_rank_given(rank):
    cnx = SQLOperations.get_connection()

    cursor = cnx.cursor()

    cursor.callproc('get_movie_of_rank', [rank])

    for res in cursor.stored_results():
        r = res.fetchall()

    for movie in r:
        print(movie[0])

    cnx.close()

    print()


def get_movies_with_actor():
    name = input("Enter the name of the actor you want to search for:\n")

    cnx = SQLOperations.get_connection()

    cursor = cnx.cursor()

    cursor.callproc('get_movies_with_actor', [name])

    for res in cursor.stored_results():
        r = res.fetchall()

    for movie in r:
        print(movie[0])

    cnx.close()

    print()


def get_actors_in_movie():
    name = input("Enter the name or rank of the movie you want to look for:\n")

    try:
        id = int(name)
    except ValueError:
        id = 0

    cnx = SQLOperations.get_connection()

    cursor = cnx.cursor()

    cursor.callproc('get_actors_in_movie', [name, id])

    for res in cursor.stored_results():
        r = res.fetchall

    for actor in r:
        print(actor[0])

    print()

    cnx.close()


def main():
    action = input("What would you like to do:\n"
                   "retrieve data\n"
                   "get movie of rank\n"
                   "get top rated movie\n"
                   "get movies with actor\n"
                   "get actors in movie\n"
                   "quit\n")

    if action == "retrieve data":
        GenericRetrieval.retrieve_info_from_table()
    elif action == "get movie of rank":
        get_movie_of_rank()
    elif action == "get top rated movie":
        get_movie_of_rank_given(1)
    elif action == "get movies with actor":
        get_movies_with_actor()
    elif action == "get actors in movie":
        get_actors_in_movie()
    elif action == "quit":
        exit(0)
    else:
        print("Please enter a valid operation.\n\n\n")

    print()

    main()


if __name__ == "__main__":
    main()
