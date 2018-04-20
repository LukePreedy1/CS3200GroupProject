from IMDbManagement.MovieAccessing import *
from SQLManagement.SQLOperations import *


def add_movie_from_id(id, rank):
    ia = imdb.IMDb()

    movie = ia.get_movie(id)

    add_movie = ("INSERT IGNORE INTO movie "
                 "(movie_id, movie_title, movie_score, movie_length, movie_language, movie_release_year")

    ia.update(movie)

    movie_title = "\"" + movie['title'] + "\""

    movie_score = float(movie['rating'])

    movie_length = movie['runtime'][0]

    try:
        movie_language = "\"" + movie['lang'][0] + "\""
    except KeyError as ke:
        print("Failed on language for show: ")
        print(movie_title)
        print("Will just set it to unlisted and just pretend.")
        movie_language = "\"unlisted\""

    movie_release_year = int(movie['year'])

    if rank != 0:
        add_movie += ", movie_rank) VALUES (%s, %s, %1.1f, %s, %s, %s, %s)"
        add_movie = add_movie % (id,
                                 movie_title,
                                 movie_score,
                                 movie_length,
                                 movie_language,
                                 movie_release_year,
                                 rank)
    else:
        add_movie += ") VALUES (%s, %s, %1.1f, %d, %s, %d)"
        add_movie = add_movie % (id,
                                 movie_title,
                                 movie_score,
                                 movie_length,
                                 movie_language,
                                 movie_release_year)

    perform_operation_on_db(add_movie)

    cast = movie['cast']

    for actor in cast:
        add_person_to_database(actor)
        add_movie_person_relationship_to_database(id, actor.getID(), '"actor"')

    print("Added movie %s\n" % movie_title)


def add_movie_person_relationship_to_database(movie_id, person_id, role):
    add_relationship = ("INSERT IGNORE INTO movie_person_relationship "
                        "(movie_id, person_id, person_role) "
                        "VALUES (%s, %s, %s)")

    relationship_results = add_relationship % (movie_id, person_id, role)
    perform_operation_on_db(relationship_results)


def initialize_movies_database():
    while True:
        try:
            num = int(input("How many movies do you want to input (up to 250):\n"))
            if num <= 0 or num > 250:
                print("Please input a valid amount.")
                continue
            break
        except ValueError:
            print("Please input a valid amount.")

    movies = get_top_number_of_movies(num)

    for i in range(0, len(movies)):
        print(movies[i])
        add_movie_from_id(movies[i], i + 1)

    print("Added all movies")


def main():
    while True:
        action = input("What do you want to do:\n"
                       "initialize database\n"
                       "quit\n\n")

        if action == "initialize database":
            initialize_movies_database()
        elif action == "quit":
            exit(0)
        else:
            print("Please enter a valid action.")


if __name__ == "__main__":
    main()