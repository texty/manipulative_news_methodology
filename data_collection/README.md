## Data collection scripts

* `crawl_htmls` - scrapy project to download articles' text and write readability html to database. If website is blocked - uses Tor and Polipo proxy
* `load_fb.py` - script to download facebook feed of a page, and store all the links in postgres. Requires facebook app, put your credentials in [`my_fb.json`](my_fb.json)
* `load_rss.py` - uses `feedparser` library to crawl RSS feeds of selected websites. Needs rewriting - on `scrapy`, and to handle blocked websites
* `sites_ids.csv` - list of all sites, its feeds and fb pages
* `ra_server.js` - express.js simple Node app. Listens to port 3000 and returns readability html. [Readability](https://github.com/mozilla/readability) is from Mozilla. Run it before launching `crawl_htmls`. To install dependencies - use `npm install` in this folder. `node ra_server.js` will launch it on port 3000
* [`../psql_engine.txt`](../psql_engine.txt) - Postgresql credentials example to use in data collection and preprocessing scripts in case you also want to store data in postgres
