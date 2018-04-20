import imdb
import requests
from bs4 import BeautifulSoup

from IMDbManagement.ShowAccessing import parse_id_from_href


def get_movie_from_title(title):
    ia = imdb.IMDb()

    res = ia.search_movie(title)

    for result in res:
        if result['kind'] == 'movie' and result['title'].lower() == title.lower():
            return result.movieID()

    return 0


def get_top_number_of_movies(num):
    url = "https://www.imdb.com/chart/top?ref_=nv_mv_250_6"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('td', class_='titleColumn')
    resulting = []

    for i in range(0, num):
        resulting.append(parse_id_from_href(results[i].find('a')['href']))

    return resulting
