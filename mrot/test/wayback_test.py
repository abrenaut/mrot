# coding: utf8
import unittest
import os
from datetime import datetime
from mrot import wayback


class TestWayback(unittest.TestCase):
    def test_list_snapshots(self):
        """
        Extract a list of memento from the resources/memento_list.txt file
        :return:
        """
        # Mock the memento URL
        wayback.MEMENTO_TEMPLATE = 'file://{memento_list}'.format(memento_list=os.path.abspath("resources/memento_list.txt"))

        # List the snapshot found in the test memento
        snapshots = wayback.list_archive('', datetime(2000, 1, 1, 0, 0), datetime(2016, 1, 1, 0, 0))

        self.assertEquals(len(snapshots), 745)

