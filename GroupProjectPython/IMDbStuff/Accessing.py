import imdb

import requests

from bs4 import BeautifulSoup

ia = imdb.IMDb()


# When given the title of a show, will return all the data we need about that show specifically
def get_show_from_title(title):
    possible_shows = ia.search_movie(title)

    # Will search through results for title, choose one that is an exact match, and then return
    for show in possible_shows:
        # Prints the name and ID if it is an exact match
        if show['title'].lower() == title.lower():
            return show

    return None


# Gets a show object, returns the IMDb url of that show
def get_url_from_show(show):
    url = "http://www.imdb.com/title/tt"
    url += str(show.getID())
    url += "/"
    return url


def get_episode_from_show(show, season_num, ep_num):
    return show['episodes'][season_num][ep_num]
