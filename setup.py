from setuptools import setup

setup(name='Csgo match result scraper',
      python_requires='>3.6.2',
      version='0.0.1',
      description='Scrapes match results from gosugamers.net, hltv.org',
      author='Aidis Stukas',
      author_email='aidiss@gmail.com',
      url='',
      packages=['scraper'],
      install_requires=['grequests', 'lxml', 'nose'],
      entry_points = {'console_scripts': ['scrape=scraper.scraper:main']}
     )
