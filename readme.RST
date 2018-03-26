====================
Mini scraping system
====================
Original task
=============
Description
-----------
A small app, show aggregated result for some game event. Reason to have more then one data source - is to make sure that data is correct and to reduce delay between actual event occurs .

Requirements
------------
Some requirements:

- [x] Use Python 3.x
- [x] Console application.
- [x] at least two data sources
- [x] Display/update screen then result change in one of the source, while providing another providers current data.
- [x] Asynchronous data read from data sources.
- [ ] websockets would be a big plus

Sources
-------
For data sources, you may use any site available via google: e-sports live score.
Also for simplicity - you can use bet odds, as there are much higher amount of sites to get data from. For example https://www.hltv.org/matches/2320359/quantum-bellator-fire-vs-enyoy-x-betco-invitational-2 they provide different  site odds in one place.


Execution could look like this::

    ./scrap "Cloud9 vs Team Liquid Map1"

or::

    ./scrap -s1 http://site1.com/cloud9-vs-team-liquid.html -s2 https://another.com/cloud9-vs-team-liquid.html

or::

    ./scrap
    choose event:
    1 Cloud9 vs Team Liquid
    2 Quantum Bellator Fire vs Enyoy
    > 1

Output could look like this::

    > 10:11:39 Cloud9 vs Team Liquid Map1 Updated: S1 0:0 -> 0:1 (S2 0:0)
    > 10:11:42 Cloud9 vs Team Liquid Map1 Updated: S2 0:0 -> 0:1 (S2 0:1)



Actual documentation
====================
Sources
-------
Lets have a look at link structure
HLTV
'https://www.hltv.org/matches/2319700/liquid-vs-faze-starseries-i-league-season-4'
{host}/matches/{match_id}/{team1_name}-vs-{team2_name}-{tournament-name}

GOSU
'https://www.gosugamers.net/counterstrike/tournaments/16628-esl-one-new-york-2017/4942-playoff/16631-bracket/matches/199617-team-liquid-vs-faze-clan', 
{host}/{game}/tournaments/{tournament_id}-{tournament_name}/{playof_id}-playoff/{id}-bracket/matches/{match_id}-{team1_name}-vs-{team2_name}


Datastructure
-------------
Analysis, required for future development. Not all fields listed bellow are used in current version.
These are the fields to scrape. All data is provided by source, (we should have our internal ids too):

- team1_name 
- team1_id
- team2_name
- team2_id
- score_match - score in rounds (1, 1) or (0, 1)
- score_rounds - ((16, 2), (0, 16)) or ((0, 16))
- status - ('complete', 'in_progress', 'not_started')
- event_name
- event_id 
- source - ('gosugamers', 'hltv')
- start_time
- scraped_time

Installation
------------
Install with pip::

    pip install git+https://github.com/aidiss/csgo_result_scraper
    
or::
    
    git clone https://github.com/aidiss/csgo_result_scraper
    cd csgo_result_scraper
    python setup.py install

Use
---
To start scraping run::

    scrape gosugamers.net/matchurl hltv.org/matchurl

This would start scraping. Results will be displayed in
command line.

Example scrape::

    scrape https://www.gosugamers.net/counterstrike/tournaments/23872-ecs-season-5/6677-regional-finals/23877-europe/matches/235650-astralis-vs-ninjas-in-pyjamas https://www.hltv.org/matches/2321241/complexity-vs-optic-dreamhack-masters-marseille-2018-north-america-closed-qualifier

Extra stuff done:
    - [x] docs (generating requires sphinx)
    - [x] tests (run with `python -m nose tests/`
