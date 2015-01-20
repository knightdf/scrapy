from scrapy.spider import Spider
from tutorial.items import BroadItem
from tutorial.itemloaders import BroadItemLoader

class BroadSpider(Spider):
    def __init__(self, name, url):
        self.name = name
        self.start_urls = [url]

    def parse(self, response):
        broadItemLoader = BBCItemLoader(item=BroadItem, response=response)
        broadItemLoader.add_xpath('title', "/html/head/title/text()")
        broadItemLoader.add_xpath('keywords', "/html/head/meta[@name='keywords']/@content")
        broadItemLoader.add_value('url', response.url)
        broadItemLoader.add_xpath('body', "/html/body/text()")
        return broadItemLoader.load_item()
