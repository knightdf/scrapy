from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings
from tutorial.spiders.broad_spider import BroadSpider
from exceptions import IOError
from multiprocessing import Process,Queue,Pool
from multiprocessing.managers import BaseManager
import os
import time

reactor.suggestThreadPoolSize(30)

class MyManager(BaseManager):
    pass

MyManager.register('Queue')

class manager(object):
    spiderCount = 0

    def __init__(self, **kw):
        self.path = kw.get('path')

    def setupCrawler(self,spider):
        crawler = Crawler(get_project_settings())
        crawler.signals.connect(self.spiderClosed, signals.spider_closed)
        crawler.configure()
        crawler.crawl(spider)
        crawler.start()

    def setupSpider(self, url):
        """
        setup spider with the given url, url can either be a list of string or a singel string
        """
        if url is not None:
            spider = None
            if isinstance(url, list):
                spider = BroadSpider(url_list=url)
            else:
                spider = BroadSpider(url=url)
            self.setupCrawler(spider)
            self.spiderCount += 1

    def spiderClosed(self):
        """
        call when spider closed
        """
        self.spiderCount -= 1
        if self.spiderCount == 0:
            reactor.stop()

    def startCrawl(self, url_list):
        """
        starting crawl
        """
        self.setupSpider(url_list)
        log.start()
        reactor.run()

    def readLines(self, line_count=1000):
        """
        a generator return @line_count lines from @self.path every time
        """
        if self.path is not None and os.path.exists(self.path):
            #the given path is a url list file
            if os.path.isfile(self.path):
                f = open(self.path, 'r')
                yield f.readlines(line_count)
            #the given path is a dir including multi url_list
            elif os.path.isdir(self.path):
                for file in os.listdir(self.path):
                    filepath = os.path.join(self.path, file)
                    if os.path.isfile(filepath):
                        f = open(filepath, 'r')
                        yield f.readlines(line_count)
        else:
            raise IOError('url list path not found!')

    def fillQueue(self, queue):
        """
        use a thread or process to put value to the queue
        """
        while True:
            try:
                q.put(f.next())
            except StopIteration:
                break

    def run(self, url_size=1000, spider_count=4):
        """
        url_size is the url list size of one spider, defaults to 1000
        spider_count is the number of spiders one time, defaults to 100
        """
        pool = Pool(spider_count)
        mgr = MyManager(address=('localhost', 12345), authkey='bilintechnology')
        server = mgr.connect()
        q = mgr.Queue()
        f = self.readLines(url_size)
        pool.apply_async(self.fillQueue, (q,))
        while not q.empty():
            #add some control on q.get() if queue is empty
            pool.map(self.startCrawl, q.get())
        pool.close()
        pool.join()


if __name__ == '__main__':
    manager = manager(path='/tmp/url_list')
    manager.run(url_size=1, spider_count=1)
