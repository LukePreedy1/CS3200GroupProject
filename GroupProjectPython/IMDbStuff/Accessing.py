import imdb

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
