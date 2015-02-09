#scrapy
scrapy projects

use `scrapy list` to see the spiders

to run scrapy from python shell but not scrapy commond, use `python run.py`

`queueManager.py` --> global Queue manager server

`urlReader.py` --> python script to read urls from given path into global queue

`run.py` --> scrapy spiders to crawl urls from global queue


**Usage**:

1.run `python queueManager.py` as a background service

2.run `python urlReader.py` to read urls

3.run `python run.py` to crawl urls

