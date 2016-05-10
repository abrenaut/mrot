# coding: utf8

import logging
import argparse
from . import imdb

logger = logging.getLogger('mrot')


def parse_args():
    parser = argparse.ArgumentParser(prog='mrot', description='Show movie ratings over time.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('movie_name', help='the name of the movie')

    # Optional arguments
    parser.add_argument("-c", "--concurrency", type=int, default=5,
                        help="maximum number of concurrent requests to the wayback machine")
    parser.add_argument("-d", "--delta", type=int, default=365, help="minimum number of days between two ratings")
    parser.add_argument("-q", "--quiet", action="store_true", help="don't print progress")

    args = parser.parse_args()

    return args


def main():
    args = parse_args()

    logging.basicConfig(level=(logging.WARN if args.quiet else logging.INFO))

    # Don't allow more than 10 concurrent requests to the wayback machine
    concurrency = min(args.concurrency, 10)

    # Find the movies corresponding to the given movie name
    imdb_movies = imdb.find_movies(args.movie_name)

    # Show rating for the first movie matching the given name
    if len(imdb_movies) > 0:
        imdb_movie = imdb_movies[0]
        imdb_movie.plot_ratings(concurrency, args.delta)
    else:
        logger.info('Movie not found')
