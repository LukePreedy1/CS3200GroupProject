import requests
from bs4 import BeautifulSoup

from IMDbStuff.Accessing import *

import mysql.connector


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
def add_show_from_id(id):
    ia = imdb.IMDb()

    show = ia.get_movie(id)

    # CANNOT ACCESS PRODUCTION COMPANY, NEED TO REMOVE!
    add_show = ("INSERT INTO tv_show "
                "(show_id, show_title, show_score, num_seasons, num_episodes, show_language) "
                "VALUES (%s, %s, %1.1f, %d, %d, %s)")

    # Need to call these before checking data.  Still not sure why, but it's important.
    ia.update(show)
    ia.update(show, 'episodes')

    # When inserting strings, they must be in quotes, otherwise it throws an error.
    # Also, python has terrible syntax for appending strings.  Just a complaint.
    show_title = "\""
    show_title += show['title']
    show_title += "\""

    show_language = "\""

    try:
        show_language += show['lang'][0]
    except KeyError as ke:
        print("Failed on language for show: ")
        print(show_title)
        print()

    show_language += "\""

    show_id = "\""
    show_id += show.movieID
    show_id += "\""

    # Chose not to make the movieID an int, since that would get rid of leading 0's
    show_result = add_show % (show_id,
                              show_title,
                              float(show['rating']),
                              int(show['seasons']),
                              int(show['number of episodes']),
                              show_language)

    # Performs the given code on the database
    perform_operation_on_db(show_result)

    # Will add all the seasons to the database
    for i in range(1, show['seasons'] + 1):
        add_season = ("INSERT INTO season "
                      "(show_id, season_num, num_episodes) " 
                      "VALUES (%s, %d, %d)")

        season_result = add_season % (show_id,
                                      i,
                                      len(show['episodes'][i]))

        perform_operation_on_db(season_result)

        # For each episode in that season, add its information to the database
        # Some shows have an episode 0, and can only be found with that.  Will use a try
        # except to make sure that it will still work.
        for j in range(0, len(show['episodes'][i]) + 1):
            try:
                add_episode_to_database(show['episodes'][i][j])
            except KeyError as ke:
                print("Show %s does not have an episode %d in season %d" % (show_title, j, i))


# Given an episode object, will add the data in the episode to the database.
def add_episode_to_database(episode):
    add_episode = ("INSERT INTO episode "
                   "(episode_id, show_id, season_num, episode_num, episode_name, length, "
                   "episode_score, director_name, air_date) "
                   "VALUES (%s, %s, %d, %d, %s, %d, %1.1f, %s, '%s'")
    return


# Returns a list strings of top 250 rated tv shows id's
# imdbpy doesn't have a way to get the top 250 specifically, so I'm going to use HTML scraping
def get_top_250():
    # URL for the page with all top 250 entries
    url = "http://www.imdb.com/chart/toptv/?ref_=nv_tvv_250_3"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('td', class_='titleColumn')
    returning = []

    for i in range(0, 250):
        returning.append(parse_id_from_href(results[i].find('a')['href']))

    return returning


# Parses the show's id from the given href.
def parse_id_from_href(href):
    ind = href.find('tt')
    return href[ind+2:ind+9]


# The Main method that will be run to make everything do what it's supposed to do
def main():
    ids = get_top_250()

    for show_id in ids:
        add_show_from_id(show_id)


if __name__ == "__main__":
    main()
