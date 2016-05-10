# coding: utf8
import unittest
import glob
from mrot import imdb


class TestMovie(unittest.TestCase):
    def test_extract_imdb_score(self):
        """
        Extract ratings from the archive stored in the resources folder
        :return:
        """
        for imdb_page_path in glob.glob('resources/imdb*.html'):
            with open(imdb_page_path) as imdb_page:
                imdb_page_content = imdb_page.read()
                movie_score = imdb.read_ratings(imdb_page_content)
                self.assertIsInstance(movie_score, float)
                self.assertTrue(5 <= movie_score <= 10)
