# coding: utf8

import logging
import re
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from PIL import Image
import urllib2
import urllib
import json
from bs4 import BeautifulSoup, element
from mrot.exceptions import ScrapeError
from mrot import wayback
from datetime import datetime

logger = logging.getLogger('mrot.imdb')

OMDB_API_TEMPLATE = 'http://www.omdbapi.com/?{query}'
IMDB_MOVIE_TEMPLATE = "http://www.imdb.com/title/{movie_id}/"


class IMDbMovie(object):
    def __init__(self, title, year, imdb_id, poster):
        self.title = title
        self.year = year
        self.imdb_id = imdb_id
        self.poster = poster

    def download_ratings(self, concurrency=5, delta=30):
        """
        Download the ratings of the movie over time
        :param concurrency: Maximum of concurrent requests to the wayback machine
        :param delta: Minimum number of days between two ratings
        :return: The ratings of the movie indexed by their date
        """
        logger.info('Downloading ratings for the movie {movie_name}.'.format(movie_name=self.title))

        # The URL for this movie on IMDb
        imdb_url = IMDB_MOVIE_TEMPLATE.format(movie_id=self.imdb_id)

        # Use the wayback machine to scrape the ratings of the movie over time
        ratings = wayback.scrape_archive(imdb_url, read_ratings, datetime(self.year, 1, 1, 0, 0), datetime.now(),
                                         concurrency, delta)

        return ratings

    def plot_ratings(self, concurrency=5, delta=30):
        """
        Show a time series representing the ratings of the movie over time
        :param concurrency: Maximum of concurrent requests to the wayback machine
        :param delta: Minimum number of days between two ratings
        """
        # Download the movie ratings
        ratings = self.download_ratings(concurrency, delta)

        # Show the ratings and the movie poster on one figure
        fig = plt.figure()

        # 1 row, 2 columns position 1
        img_fig = fig.add_subplot(121)
        # Hide axis around the poster
        img_fig.axes.get_xaxis().set_visible(False)
        img_fig.axes.get_yaxis().set_visible(False)
        # Show the poster on the first column
        f = urllib2.urlopen(self.poster)
        img = Image.open(f)
        img_fig.imshow(img)

        # 1 row, 2 columns position 2
        ratings_fig = fig.add_subplot(122)
        # Show ratings on the second column
        sorted_keys = sorted(ratings.keys())
        axis_values = mdates.date2num(sorted_keys)
        ratings_fig.plot_date(x=axis_values, y=[ratings[key] for key in sorted_keys], fmt="r-")
        ratings_fig.set_title('Ratings of the movie "{title}" over time'.format(title=self.title))
        ratings_fig.set_ylabel("Ratings")
        # Set the range of the y value to (min_rating - 1), (max_rating + 1)
        ratings_fig.set_ylim([max(min(ratings.values()) - 1, 0), min(max(ratings.values()) + 1, 10)])

        # Show the figure
        plt.show()


def find_movies(movie_name):
    """
    Find the movies corresponding to the given movie name
    :param movie_name:
    :return: A list of movies
    """
    logger.info('Searching for movies named {movie_name}.'.format(movie_name=movie_name))
    movies = []

    # Query OMDb API with the given movie name
    api_response = query_search_api(s=movie_name, type_filter='movie')

    if api_response['Response'] == 'True':
        movies += [IMDbMovie(movie['Title'], int(movie['Year']), movie['imdbID'], movie['Poster']) for
                   movie in api_response['Search']]

    return movies


def query_search_api(s='', type_filter='movie'):
    """
    Query OMDb API to obtain movie information
    :param s: Movie title to search for.
    :param type_filter: Type of result to return.
    :return:
    """
    query = urllib.urlencode({'s': s, 'type': type_filter})

    omdb_api_url = OMDB_API_TEMPLATE.format(query=query)
    req = urllib2.Request(omdb_api_url)

    # Read and decode the API response
    response_json = urllib2.urlopen(req).read().decode("utf-8")
    response = json.loads(response_json)

    return response


def read_ratings(imdb_page_content):
    """
    Extract a movie rating from its imdb page
    :param imdb_page_content:
    :return:
    """
    soup = BeautifulSoup(imdb_page_content, 'html.parser')

    ratings_element = soup.find('span', itemprop="ratingValue")
    if ratings_element is not None and ratings_element.string != '-':
        return float(ratings_element.string.replace(',', '.'))

    ratings_element = soup.find('div', class_="star-box-giga-star")
    if ratings_element is not None:
        return float(ratings_element.string)

    ratings_element = soup.find('span', class_="rating-rating")
    if ratings_element is not None:
        if type(ratings_element.contents[0]) is element.NavigableString:
            return float(ratings_element.contents[0].string)
        else:
            return float(ratings_element.span.string)

    # Fallback, find a string matching "float/10"
    ratings_ovr_ten = soup.find(string=re.compile("^[\d\.]+/10$"))
    if ratings_ovr_ten is not None:
        return float(ratings_ovr_ten.string.split('/')[0])

    raise ScrapeError('Could not extract ratings')
