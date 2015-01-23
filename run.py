from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings
from tutorial.spiders.broad_spider import BroadSpider
from exceptions import IOError
from multiprocessing import Process
import os

reactor.suggestThreadPoolSize(30)

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

    def setupSpider(self, url):
        if url is not None:
            spider = BroadSpider(url=url)
            self.setupCrawler(spider)
            self.spiderCount += 1

    def spiderClosed(self):
        self.spiderCount -= 1
        if self.spiderCount == 0:
            reactor.stop()

    def run(self):
        if self.path is not None and os.path.exists(self.path):
            #the given path is a url list file
            if os.path.isfile(self.path):
                for line in open(self.path):
                    self.setupSpider(line)
            #the given path is a dir including multi url_list
            elif os.path.isdir(self.path):
                for file in os.listdir(self.path):
                    filepath = os.path.join(self.path, file)
                    if os.path.isfile(filepath):
                        for line in open(filepath):
                            self.setupSpider(line)
            log.start()
            reactor.run()
        else:
            raise IOError('url list path not found!')

if __name__ == '__main__':
    manager = manager(path='/tmp/url_list')
    manager.run()
