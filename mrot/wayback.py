# coding: utf8

import logging
import urllib2
import re
from datetime import datetime
from mrot.exceptions import ScrapeError
from multiprocessing.pool import ThreadPool

logger = logging.getLogger('mrot.wayback')

MEMENTO_TEMPLATE = "https://web.archive.org/web/timemap/link/{url}"
MEMENTO_ARCHIVE_PAT = '^<(http://web.archive.org/web/\d+/.*)>; rel="(first\s|last\s)?memento"; datetime="(.+)",?$'
MEMENTO_DATE_FORMAT = "%a, %d %b %Y %H:%M:%S GMT"


class Archive:
    def __init__(self, date, url):
        self.date = date
        self.url = url


def scrape_archive(url, scrape_function, min_date, max_date, concurrency=5, delta=30):
    """
    Scrape the given URL archives using the given function
    :param url:
    :param scrape_function:
    :param min_date: The archives minimum date
    :param max_date: The archives maximum date
    :param concurrency: Maximum of concurrent requests to the wayback machine
    :param delta: Minimum number of days between two archive
    :return: The results of the scrape function for each archive indexed by their date
    """
    result = {}

    # Get the list of archive available for the given url
    archive_list = list_archive(url, min_date, max_date)

    # Filter the archive list to have a minimum number of days between each archive
    filtered_archive_list = filter_archive_list(archive_list, delta)

    def scrape(archive):
        logger.info('Scraping the archive {archive_url}'.format(archive_url=archive.url))
        try:
            # Download archive content
            archive_content = download(archive.url)
            # Apply the scape function to the archive
            scrape_result = scrape_function(archive_content)
            # Index the result by the archive date
            result[archive.date] = scrape_result
        except ScrapeError, e:
            logger.info('Could not scrape the archive {url} : {msg}'.format(url=archive.url, msg=str(e)))
        except urllib2.HTTPError, e:
            logger.info('Could not download the archive {url} : {msg}'.format(url=archive.url, msg=str(e)))

    # Launch multiple scraping in parallel
    pool = ThreadPool(concurrency)
    try:
        pool.map(scrape, filtered_archive_list)
    finally:
        pool.close()
        pool.join()

    return result


def list_archive(url, min_date, max_date):
    """
    List the available archive between start_date and end_date for the given URL
    :param url:
    :param min_date: The archives minimum date
    :param max_date: The archives maximum date
    :return:
    """
    logger.info('Listing the archives between {min_date} and {max_date} for the url {url}'.format(min_date=min_date,
                                                                                                  max_date=max_date,
                                                                                                  url=url))
    # Download the memento list
    memento_list_url = MEMENTO_TEMPLATE.format(url=url)
    memento_list = download(memento_list_url)

    # Parse the memento to extract the list of archive
    lines = memento_list.split("\n")
    prog = re.compile(MEMENTO_ARCHIVE_PAT.format(url=url))
    matches = filter(None, (re.search(prog, line) for line in lines))
    archive_list = [Archive(datetime.strptime(m.group(3), MEMENTO_DATE_FORMAT), m.group(1)) for m in matches]

    # Filter the archive list to keep only the one between min_date and max_date
    archive_list = [archive for archive in archive_list if min_date < archive.date < max_date]

    logger.info(
            'Found {count} archives between {min_date} and {max_date} for the url {url}'.format(count=len(archive_list),
                                                                                                min_date=min_date,
                                                                                                max_date=max_date,
                                                                                                url=url))

    return archive_list


def filter_archive_list(archive_list, delta):
    """
    Filter a list of archive in order to have a minimum number of days between each archive
    :param archive_list:
    :param delta:
    :return:
    """
    filtered_archive_list = []

    # Sort the list of archive by their date
    archive_list.sort(key=lambda x: x.date)

    # For each archive, make sure there is a minimum of days between the archive and the previous archive in the list
    prev_date = None
    for archive in archive_list:
        if prev_date is None or (archive.date - prev_date).days > delta:
            filtered_archive_list.append(archive)
            prev_date = archive.date
    return filtered_archive_list


def download(url):
    logger.debug('Downloading the content of the url {url}'.format(url=url))

    req = urllib2.Request(url, None, {'User-Agent': 'Mozilla/5.0'})
    content = urllib2.urlopen(req).read().decode("utf-8")

    return content
