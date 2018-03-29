import imdb
import requests
from bs4 import BeautifulSoup

ia = imdb.IMDb()


# When given the title of a show, will return all the data we need about that show specifically
def get_show_from_id(id):
    possible_shows = ia.search_movie(title)


    # Will search through results for title, choose one that is an exact match, and then return
    for show in possible_shows:
        # Returns the show object if the titles match, ignoring case
        # Also checks that it is actually a show or miniseries.  Otherwise
        # movies with the same name would be chosen instead
        if (show['kind'] == 'tv series' or show['kind'] == 'tv miniseries') and show['title'].lower() == title.lower():
            return show
        else:
            print(title)
            print(show['title'])

    return None


def get_episode_from_show(show, season_num, ep_num):
    return show['episodes'][season_num][ep_num]


# Parses the show's id from the given href.
def parse_id_from_href(href):
    ind = href.find('tt')
    return href[ind+2:ind+9]


# Returns a list strings of top 100 rated tv shows id's.
# imdbpy doesn't have a way to get the top 100 specifically, so I'm going to use HTML scraping.
# I was going to do top 250, but that was taking >1hour to run, so this is just making my life easier.
def get_top_100():
    # URL for the page with all top 100 entries
    url = "http://www.imdb.com/chart/toptv/?ref_=nv_tvv_250_3"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('td', class_='titleColumn')
    returning = []

    for i in range(0, 100):
        returning.append(parse_id_from_href(results[i].find('a')['href']))

    return returning
