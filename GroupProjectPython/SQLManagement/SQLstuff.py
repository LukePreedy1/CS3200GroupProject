from IMDbStuff.Accessing import *
import mysql.connector

cnx = mysql.connector.connect(user='root', password='Yourface1234',
                              host='127.0.0.1',
                              database='imdb_group_project')


# Gets the title of the show as a string, adds the show to the database.  does not return
def add_show_from_title(title):
    ia = imdb.IMDb()

    show = get_show_from_title(title)

    # CANNOT ACCESS PRODUCTION COMPANY, NEED TO REMOVE!
    add_show = ("INSERT INTO tv_show "
                "(show_id, show_title, show_score, num_seasons, num_episodes, show_language) "
                "VALUES (%d, %s, %d, %d, %d, %s)")

    # Need to call this before checking data.  Still not sure why, but its important.
    ia.update(show)

    print(show['kind'])

    print(show['seasons'])
    print(show['rating'])

    # need to call before checking episode data
    ia.update(show, 'episodes')

    print(type(show.getID()))

    print(add_show % (int(show.movieID),
                      show['title'],
                      float(show['rating']),
                      int(show['seasons']),
                      int(show['number of episodes']),
                      show['lang'][0]))


# Example demonstrating it works as intended
add_show_from_title('breaking bad')

