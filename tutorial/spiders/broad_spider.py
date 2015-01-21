from scrapy.spider import Spider
from tutorial.items import BroadItem
from tutorial.itemloaders import BroadItemLoader
from scrapy.log import log

class BroadSpider(Spider):
    name = 'broad'

    def __init__(self, **kw):
        super(BroadSpider, self).__init__(**kw)
        url = kw.get('url')
        if not (url.startswith('http://') or url.startswith('https://')):
            url = 'http://%s'%url
        self.start_urls = [url]

    def parse(self, response):
        broadItemLoader = BroadItemLoader(item=BroadItem(), response=response)
        broadItemLoader.add_xpath('title', "/html/head/title/text()")
        broadItemLoader.add_xpath('keywords', "/html/head/meta[@name='keywords']/@content")
        broadItemLoader.add_value('url', unicode(response.url))
        broadItemLoader.add_xpath('body', "/html/body")
        return broadItemLoader.load_item()
