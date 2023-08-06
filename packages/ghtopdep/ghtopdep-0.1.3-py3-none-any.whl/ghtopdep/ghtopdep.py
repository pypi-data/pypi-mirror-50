from collections import namedtuple
from operator import attrgetter
import calendar
from datetime import datetime, timedelta
from email.utils import parsedate, formatdate

import click
import requests
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache
from cachecontrol.heuristics import BaseHeuristic
from halo import Halo
from selectolax.parser import HTMLParser
from tabulate import tabulate

NEXT_BUTTON_SELECTOR = '#dependents > div.paginate-container > div > a'
ITEM_SELECTOR = '#dependents > div.Box > div.flex-items-center'
REPO_SELECTOR = 'span > a.text-bold'
STARS_SELECTOR = 'div > span:nth-child(1)'
GITHUB_URL = 'https://github.com'


class OneDayHeuristic(BaseHeuristic):

    def update_headers(self, response):
        date = parsedate(response.headers["date"])
        expires = datetime(*date[:6]) + timedelta(days=1)
        return {
            "expires": formatdate(calendar.timegm(expires.timetuple())),
            "cache-control": "public",
        }

    def warning(self, response):
        msg = "Automatically cached! Response is Stale."
        return '110 - "%s"' % msg


@click.command()
@click.argument('url')
@click.option('--show', default=10, help='Number of showing repositories (default=10).')
@click.option('--more-than', default=5, help='Minimum number of stars (default=5).')
def cli(url, show, more_than):
    url = '{}/network/dependents'.format(url)
    Repo = namedtuple('Repo', ['url', 'stars'])
    repos = []
    more_than_zero = 0
    repo_count = 0
    spinner = Halo(text='Fetch information about dependents repo', spinner='dots')
    spinner.start()
    sess = requests.session()
    cached_sess = CacheControl(sess, cache=FileCache(".ghtopdep_cache"), heuristic=OneDayHeuristic())
    while True:
        r = cached_sess.get(url)
        parsed_node = HTMLParser(r.text)
        dependents = parsed_node.css(ITEM_SELECTOR)
        repo_count += len(dependents)
        for i in dependents:
            repo_stars = i.css(STARS_SELECTOR)[0].text().strip()
            repo_stars_num = int(repo_stars.replace(',', ''))
            if repo_stars_num != 0:
                more_than_zero += 1
            if repo_stars_num >= more_than:
                relative_repo_url = i.css(REPO_SELECTOR)[0].attributes['href']
                repo_url = '{}{}'.format(GITHUB_URL, relative_repo_url)
                repos.append(Repo(repo_url, repo_stars_num))

        node = parsed_node.css(NEXT_BUTTON_SELECTOR)
        if len(node) == 2:
            url = node[1].attributes['href']
        elif len(node) == 0 or node[0].text() == "Previous":
            spinner.stop()
            break
        elif node[0].text() == "Next":
            url = node[0].attributes['href']

    sorted_repos = sorted(repos[:show], key=attrgetter('stars'), reverse=True)
    print(tabulate(sorted_repos, headers=['URL', "Stars"], tablefmt="grid"))

    print('found {} repos others repos is private'.format(repo_count))
    print('found {} repos with more than zero star'.format(more_than_zero))
