import unittest
from scraper import scraper
import datetime
import collections
class TestScrapeHltv(unittest.TestCase):
    """New stuff"""
    def test_parse_normal(self):
        """Scrape hltv"""
        expected = {}
        response_body = '<html></html>'
        with open('tests/fixtures/hltv.html') as f:
            html = f.read()
        result = scraper.scrape_hltv(html)
        expected = {
            'team1': 'compLexity', 
            'team2': 'OpTic', 
            'scores': [(16, 13), (16, 11)], 
            'source': 'hltv', 
            'status': 'LIVE',
            'time': '',
            }
        self.assertEqual(dict(result), expected)


class TestScrapeGosu(unittest.TestCase):
    def test_parse_normal(self):
        """Scrape gosugamers"""
        expected = {}
        with open('tests/fixtures/gosu.html') as f:
            html = f.read()
        result = scraper.scrape_gosugamers(html)
        expected = {
            'team1': 'Astralis', 
            'team2': 'Ninjas in Pyjamas', 
            'scores': [(19, 17)], 
            'source': 'gosugamers', 
            'winners': ['Astralis'],
            'time': '',
            }
        print(dict(result))
        self.assertEqual(dict(result), expected)
