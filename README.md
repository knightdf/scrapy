#scrapy 
scrapy projects

use 'scrapy list' to see the spiders

to run scrapy from python shell but not scrapy commond, use `python run.py`

queueManager.py --> global Queue manager server
urlReader.py --> python script to read urls from given path into global queue
run.py --> scrapy spiders to crawl urls from global queue

Usage:
1,run queueManager.py as a background service
2,run urlReader.py to read urls
3,run run.py to crawl urls
