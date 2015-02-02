from scrapy.spider import Spider
from tutorial.items import BroadItem
from tutorial.itemloaders import BroadItemLoader
from scrapy.log import log

class BroadSpider(Spider):
    name = 'broad'

    def __init__(self, **kw):
        """
        BroadSpider can be initilized either by a single url(take first) or a url list
        """
        super(BroadSpider, self).__init__(**kw)
        url = kw.get('url')
        url_list = kw.get('url_list')
        if url != None:
            self.start_urls = [url]
        elif url_list != None:
            self.start_urls = url_list

    def parse(self, response):
        broadItemLoader = BroadItemLoader(item=BroadItem(), response=response)
        broadItemLoader.add_xpath('title', "/html/head/title/text()")
        broadItemLoader.add_xpath('keywords', "/html/head/meta[@name='keywords']/@content")
        broadItemLoader.add_value('url', unicode(response.url))
        broadItemLoader.add_xpath('body', "/html/body")
        return broadItemLoader.load_item()
