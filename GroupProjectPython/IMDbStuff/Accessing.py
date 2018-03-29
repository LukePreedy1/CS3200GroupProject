import imdb
import requests
from bs4 import BeautifulSoup

ia = imdb.IMDb()


# Parses the show's id from the given href.
def parse_id_from_href(href):
    ind = href.find('tt')
    return href[ind+2:ind+9]


# Returns a list strings of top 100 rated tv shows id's.
# imdbpy doesn't have a way to get the top 100 specifically, so I'm going to use HTML scraping.
# I was going to do top 250, but that was taking >1hour to run, so this is just making my life easier.

# I'm reducing it down to 10 for testing, will restore it when the program is finished.
def get_top_100():
    # URL for the page with all top 100 entries
    url = "http://www.imdb.com/chart/toptv/?ref_=nv_tvv_250_3"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('td', class_='titleColumn')
    returning = []

    for i in range(0, 10):
        returning.append(parse_id_from_href(results[i].find('a')['href']))

    return returning
