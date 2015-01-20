from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings
from tutorial.spiders.broad_spider import BroadSpider
from exceptions import IOError
import os

class manager(object):
    spiderCount = 0

    def __init__(self, **kw):
        self.path = kw.get('path')

    def setupCrawler(self, spider):
        crawler = Crawler(get_project_settings())
        crawler.signals.connect(self.spiderClosed, signals.spider_closed)
        crawler.configure()
        crawler.crawl(spider)
        crawler.start()

    def setupSpider(self, path):
        if os.path.exists(path):
            for line in open(path):
                spider = BroadSpider(url=line)
                self.setupCrawler(spider)
                self.spiderCount += 1
        else:
            raise IOError('path not exists')

    def spiderClosed(self):
        self.spiderCount -= 1
        if self.spiderCount == 0:
            reactor.stop()

    def run(self):
        if self.path is not None:
            self.setupSpider(self.path)
            log.start()
            reactor.run()

if __name__ == '__main__':
    manager = manager(path='/tmp/url_list')
    manager.run()
