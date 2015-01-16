from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from tutorial.items import BBCItem
from tutorial.itemloaders import BBCItemLoader

class BBCSpider(CrawlSpider):
    name = 'bbc'
    allowed_domains = ['bbc.com']
    start_urls = ['http://www.bbc.com/']
    rules = [Rule(LxmlLinkExtractor(allow=['^http://www.bbc.com/\w+?/.*']), callback='parse_body', follow=True)]

    def parse_body(self, response):
        bbc = BBCItemLoader(item = BBCItem(), response = response)
        bbc.add_value('postId', unicode(response.url))
        bbc.add_xpath('title', "//*[@id='main-content']/div[@class='layout-block-a']/div[@class='story-body']/h1[@class='story-header']/text()")
        bbc.add_xpath('content', "//*[@id='main-content']/div[@class='layout-block-a']/div[@class='story-body']/p/text()")
        bbc.add_xpath('time', "//*[@id='main-content']/div[@class='layout-block-a']/div[@class='story-body']/span[@class='story-date']/span[@class='date']/text()")
        bbc.add_value('url', unicode(response.url))
        bbc.add_value('channel', unicode(response.url))
        bbc.add_xpath('keywords', "/html/head/meta[@name='keywords']/@content")
        return bbc.load_item()
