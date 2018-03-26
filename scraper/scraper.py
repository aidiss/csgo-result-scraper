"""Esport result scraper

Scrapes esports results.

Disciplines supported:
    csgo (default)

Fields scraped:
    Team names
    Total result

Supported websites: gosugamers.net, hltv.org.
Example::

    $ scrape gosugamers.com htlv.com

ToDo::
        - Create url parser. urls contain a lot of information
        - Create event scraper. Scraper particulat event by name or by id.
        - Use web sockets provided by the websites.
"""

import argparse
import collections
import datetime
import grequests
import logging
import lxml.html
import requests
import time
import os
import sys

TIMEOUT = 0.5
SLEEP_SECONDS = 10
MAX_ITERATIONS = 50 

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('urls', nargs='+', help='list of urls separated by space')
    parser.add_argument('-e', '--event', help='NOT IMPLEMENTED YET. Event name or id')
    parser.add_argument('--t1', help='NOT IMPLEMENTED YET. team1 name or id')
    parser.add_argument('--t2', help='NOT IMPLEMENTED YET. team2 name or id')
    parser.add_argument('-d', '--debug', help='increase output verbosity', action='store_true')
    parser.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)
    
    if args.verbose:
        logging.basicConfig(level='INFO')
    elif args.debug:
        logging.basicConfig(level='DEBUG')
    global logger
    logger = logging.getLogger(name=__name__)

    try:
        file_handler = logging.FileHandler('/var/log/scraper.log', mode='a', encoding=None, delay=False)
        logger.addHandler(file_handler)
    except:
        logger.info('Logging filehandler failed to initialized. Please root.')

    stream_handler = logging.StreamHandler()
    logger.addHandler(stream_handler)

    scrape_csgo(args)

def scrape_csgo(args):
    """Main entrypoint"""

    n = 0
    urls = [x for x in args.urls if 'gosugamers' in x or 'hltv.org' in x] 
    while True:
        try:
            parse_urls(urls)
            n += 1
            if n == MAX_ITERATIONS:
                #os.system('clear')
                #sys.stdout.write('\r\r'.ljust(100))
                break
            else:
                sys.stdout.write('\033[F\033[F')
                time.sleep(SLEEP_SECONDS)
        except (KeyboardInterrupt, SystemExit) as e:
            sys.exit(e)


def parse_urls(urls: list):
    """Parse list of urls.

    Returns urls that are valid, scrapers ready.
    """
    rs = (grequests.get(u, timeout=TIMEOUT) for u in urls)
    responses = grequests.map(rs, exception_handler=exception_handler)
    results = [{}, {}]
    for r in responses:
        if not r:
            continue

        if 'www.gosugamers.net' in r.url:
            d = scrape_gosugamers(r.text)
            d['time'] = datetime.datetime.now()
            results[0] = d

        elif 'www.hltv.org' in r.url:
            d = scrape_hltv(r.text)
            d['time'] = datetime.datetime.now()
            results[1] = d
    try:
        output_result(results)
    except:
        sys.exit('Cant scrape :(')


def scrape_hltv(response_body: str) -> collections.defaultdict:
    """Scrape hltv org

    Returns:
        a result dict.
    """
    d = collections.defaultdict(team1='', team2='', scores=[], source='', time='')
    d['source'] = 'hltv'

    etree = lxml.html.fromstring(response_body).getroottree()

    a = etree.xpath('//div[@class="mapholder"]/div[@class="results"]/span[@class="won"]/text()')
    a = [int(x) for x in a]
    b = etree.xpath('//div[@class="mapholder"]/div[@class="results"]/span[@class="lost"]/text()')
    b = [int(x) for x in b]
    d['scores'] = list(zip(a, b))

    teams = etree.xpath('//div[@class="teamName"]/text()')
    d['team1'], d['team2'] = teams

    d['status'] = etree.xpath("//div[@class='countdown']/text()")[0]
    #d['status'] = "bestof"
    return d


def scrape_gosugamers(response_body: str) -> collections.defaultdict:
    """Scrape gosugamers.net.

    Returns:
        a result dict.
    """
    d = collections.defaultdict(team1='', team2='', scores=[], source='', time='')
    d['source'] =  'gosugamers'

    etree = lxml.html.fromstring(response_body).getroottree()
    d['team1'] = etree.xpath('//div[@class="opponent opponent1"]/h3/a/text()')[0]
    d['team2'] = etree.xpath('//div[@class="opponent opponent2"]/h3/a/text()')[0]

    scores = etree.xpath('//div[@class="roundset totals"]/span/text()')
    scores = [int(x) for x in scores]
    scores = list(zip(scores[::2], scores[1::2]))
    d['scores'] = [x for x in scores]

    winners = etree.xpath('//div[@class="matches-streams"]/span/input[@class="btn-winner"]/@value')
    d['winners'] = [x.replace('Winner: ', '') for x in winners]
    return d


def download_page(url: str) -> requests.Response:
    """Downloads a page"""
    try:
        r = requests.get(url)
        return r
    except Exception as e:
        raise e
    

def output_result(results: list):
    """Prints out results"""
    d, d1 = results
    try:
        d['time'] = d['time'].strftime('%Y-%m-%d %H:%M')
        d1['time'] = d1['time'].strftime('%Y-%m-%d %H:%M')
        message = '{time}, {source}, {team1} vs {team2}: {scores}'.format(**d).ljust(100)
        message1 = '{time}, {source}, {team1} vs {team2}: {scores}'.format(**d1).ljust(100)
        sys.stdout.write(message + '\n' + message1 + '\n')
    except Exception as e:
        raise e


def exception_handler(request, exception):
    if exception:
        logger.exception(exception)
    pass
