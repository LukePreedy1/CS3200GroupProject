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


# Since IMDbPY doesn't allow you to check the score, I'm just going to use BeautifulSoup to HTML
# scrape the information off the site directly
# Recieves a show object, returns a float
def imdb_show_score_getter(show):
    try:
        url = requests.get(get_url_from_show(show))
        soup = BeautifulSoup(url.content, 'html.parser')

        result = soup.find('div', class_='ratingValue')     # Finds where in the HTML the score is stored

        score = result.strong.span.text  # gets the score as a string

        return float(score)   # converts the score into a float

    except AttributeError:
        # This should not happen, since all the top 250 should have a score.  It's just here
        # as a safeguard.
        print("AttributeError.  This is happening because the show does not have a score.\n")
        return float(-1)


def get_episode_from_show(show, season_num, ep_num):
    return show['episodes'][season_num][ep_num]


print(imdb_show_score_getter(get_show_from_title("twin peaks")))