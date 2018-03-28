from IMDbStuff.Accessing import *

import mysql.connector


# Gets the title of the show as a string, adds the show to the database.  does not return
def add_show_from_title(title):
    ia = imdb.IMDb()

    show = get_show_from_title(title)

    # CANNOT ACCESS PRODUCTION COMPANY, NEED TO REMOVE!
    add_show = ("INSERT INTO tv_show "
                "(show_id, show_title, show_score, num_seasons, num_episodes, show_language) "
                "VALUES (%s, %s, %1.1f, %d, %d, %s)")

    # Need to call these before checking data.  Still not sure why, but it's important.
    ia.update(show)
    ia.update(show, 'episodes')

    # When inserting strings, they must be in quotes, otherwise it throws an error
    # Also, python has terrible syntax for appending strings.  Just a complaint
    show_title = "'"
    show_title += show['title']
    show_title += "'"

    show_language = "'"
    show_language += show['lang'][0]
    show_language += "'"

    show_id = "'"
    show_id += show.movieID
    show_id += "'"

    print(float(show['rating']))

    # Chose not to make the movieID an int, since that would get rid of leading 0's
    result = add_show % (show_id,
                         show_title,
                         float(show['rating']),
                         int(show['seasons']),
                         int(show['number of episodes']),
                         show_language)

    print(result)

    cnx = mysql.connector.connect(user='root',
                                  password='Yourface1234',
                                  host='127.0.0.1',
                                  database='imdb_group_project')

    cursor = cnx.cursor()

    try:
        cursor.execute(result)
        cnx.commit()
    except mysql.connector.Error as err:
        print("Could not insert the Show into the database")
        print(err.msg)
        exit(1)

    cnx.close()


# Example demonstrating it works as intended
add_show_from_title('twin peaks')

