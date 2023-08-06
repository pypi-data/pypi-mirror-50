# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from logging import getLogger
import sys
try:
    from urllib.request import urlopen
    from urllib.parse import quote, urlparse, parse_qs
except:
    # python 2
    from urllib2 import urlopen  
    from urllib import quote 
    from urlparse import urlparse, parse_qs
from bs4 import BeautifulSoup as bs

logger = getLogger(__name__)

def scrape_episode_scripts(show, season, episode):
    baseurl = "https://www.springfieldspringfield.co.uk/view_episode_scripts.php?tv-show=%s&episode=s%02de%02d"
    url = baseurl % (show, season, episode)
    #print("Reading {} ...".format(url))

    x = urlopen(url).read()
    soup = bs(x, features="html5lib")

    div = soup.find("div", "main-content-left")
    if div is None:
        print("Filed scraping")
        return None, None

    title = div.find("h3")
    if title is None:
        print("Failed to find episode title")
        title = "TITLE NOT FOUND"
    else:
        title = title.text

    script = div.find("div", "scrolling-script-container")
    if script is None:
        print("Failed to find script")
        script = "SCRIPT NOT FOUND"
    else:
        for br in script.find_all("br"):
            br.replace_with("\n")
        script = script.get_text().strip()

    return title, script



def search_shows(keyword):
    baseurl = "https://www.springfieldspringfield.co.uk/tv_show_episode_scripts.php?search=%s"
    url = baseurl % quote(keyword)
    logger.debug("Reading %s", url)
    x = urlopen(url).read()
    soup = bs(x, features="html5lib")

    # find the page count
    pagination = soup.find("div", {"class":"pagination"})
    if pagination is None:
        logger.error("Page links not found")
        return [] 
    pagelinks = pagination.find_all("a")
    pagelinks = [page.get("href") for page in pagelinks if page.has_attr("href")] 
    pagelinks = [page for page in pagelinks if page.find("page=") > 0]
    maxpage = len(pagelinks) + 1  # add 1 because the current page (i.e. first page) has not link
    logger.debug("Max page is %d", maxpage)

    # loop over pages
    shows = []
    baseurl = url 
    for page in range(1, maxpage + 1):
        # find the shows in this page and append
        items = soup.find_all("a", {"class":"script-list-item"})
        items = [i for i in items if i.has_attr("href")]
        names = [i.text for i in items] 
        links = [i.get("href") for i in items] 
        ids = [parse_qs(urlparse(l).query).get("tv-show") for l in links]
        items = [(n, i[0]) for n, i in zip(names, ids) if len(i) > 0 and len(n) > 0] 
        shows = shows + items

        if page >= maxpage:
            break

        # get the next page
        url = baseurl + ("&page=%d" % (page + 1))  # done with page, so next is page + 1 
        logger.debug("Reading %s", url)
        x = urlopen(url).read()
        soup = bs(x, features="html5lib")
    shows = list(set(shows))  # remove duplicates 
    shows.sort()
    return shows 



def episode_script_command():
    parser = ArgumentParser(description="TV Show Script")
    parser.add_argument("show", type=str, help="TV show id. If `--search`, used as the keyword")
    parser.add_argument("season", type=int, nargs="?", default=1, help="Season number (default=1)")
    parser.add_argument("episode", type=int, nargs="?", default=1, help="Episode number (default=1)")
    parser.add_argument("--search", action="store_true", help="Search shows by keyword")
    args = parser.parse_args()

    if args.search:
        print("* Searching TV shows with keyword `%s`..." % args.show)
        shows = search_shows(args.show)
        print("%d match" % len(shows))
        lens = (5, 5)
        for show in shows:
            lens = max(lens[0], len(show[0])), max(lens[1], len(show[1]))

        fmt = " %%%ds | %%%ds" % lens
        print(fmt % ("title", "id"))
        print(" " + ("-" * (sum(lens) + 3)))
        for show in shows:
            print(fmt % show)
        print(" " + ("-" * (sum(lens) + 3)))
        return 0

    else:
        print("TV show script for {}, Season {}, Episode {}".format(args.show, args.season, args.episode))
        sys.stdout.flush()
        title, script = scrape_episode_scripts(args.show, args.season, args.episode)
        print("-------------------------------------------------")
        print(title)
        print("-------------------------------------------------")
        print(script)
        print("-------------------------------------------------")

        return 0


