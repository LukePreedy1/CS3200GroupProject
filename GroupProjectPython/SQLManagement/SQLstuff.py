from IMDbStuff.Accessing import *
import mysql.connector

cnx = mysql.connector.connect(user='root', password='Yourface1234',
                              host='127.0.0.1',
                              database='imdb_group_project')


# Gets the title of the show as a string, adds the show to the database.  does not return
def add_show_from_title(title):
    ia = imdb.IMDb()

    show = get_show_from_title(title)

    add_show = ("INSERT INTO tv_show "
                "(show_id, show_title, show_score, num_seasons, num_episodes, show_language, studio_name) "
                "VALUES (%d, %s, %d, %d, %d, %s, %s)")

    imdb_show_score_getter(show)
    #ia.update(show.movieID, ['main', 'vote details'])

    print(show['kind'])

    print(show['number of episodes'])

    #print(add_show % (show.movieID, show['title'], imdb_show_score_getter(show), show['']))


add_show_from_title('breaking bad')

