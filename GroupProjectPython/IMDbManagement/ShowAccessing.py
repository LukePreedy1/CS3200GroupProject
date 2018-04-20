import imdb
import requests
from bs4 import BeautifulSoup

ia = imdb.IMDb()


# Parses the show's id from the given href.
def parse_id_from_href(href):
    ind = href.find('tt')
    return href[ind+2:ind+9]


def get_show_from_title(title):
    ia = imdb.IMDb()

    res = ia.search_movie(title)

    for result in res:
        if result['kind'] == 'tv series' and result['title'].lower() == title.lower():
            return result.movieID

    return 0


# Returns a list strings of top given number ranked tv shows, in the order of their rank on IMDb
def get_top_number_of_shows(num):
    # URL for the page with all top 100 entries
    url = "http://www.imdb.com/chart/toptv/?ref_=nv_tvv_250_3"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('td', class_='titleColumn')
    returning = []

    for i in range(0, num):
        returning.append(parse_id_from_href(results[i].find('a')['href']))

    return returning
