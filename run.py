from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings
from tutorial.spiders.broad_spider import BroadSpider
from exceptions import IOError
from multiprocessing.managers import BaseManager
import multiprocessing as mul
import time

reactor.suggestThreadPoolSize(30)

class MyManager(BaseManager):
    pass

MyManager.register('Queue')

class Manager(object):
    spiderCount = 0

    def __init__(self, spider_count=mul.cpu_count()):
        """
        set up scrapy manager with using a @spider_count process pool
        """
        self._spider_count = spider_count
        mgr = MyManager(address=('localhost', 12345), authkey='bilintechnology')
        server = mgr.connect()
        self._queue = mgr.Queue()
        # due to a bug of python's manager/proxy, see `http://bugs.python.org/issue7503` for details
        mul.current_process().authkey = 'bilintechnology'

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

    def run(self):
        """
        using a process pool at size of self._spider_count
        """
        pool = mul.Pool(self._spider_count)
        while not self._queue.empty():
            #add some control on q.get() if queue is empty
            pool.apply_async(self.startCrawl, (self._queue.get(),))
        pool.close()
        pool.join()


if __name__ == '__main__':
    manager = Manager(spider_count=2)
    manager.run()
