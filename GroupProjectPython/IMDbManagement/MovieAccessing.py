import imdb
import requests
from bs4 import BeautifulSoup


def get_movie_from_title(title):
    ia = imdb.IMDb()

    res = ia.search_movie(title)

    for result in res:
        if result['kind'] == 'movie' and result['title'].lower() == title.lower():
            return result.movieID()

    return 0




