from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from tutorial.items import TorrentItem

class TorrentSpider(CrawlSpider):
    name = "torrents"
    allowed_domains = ['mininova.org']
    start_urls = ['http://www.mininova.org/today']
    rules = [Rule(SgmlLinkExtractor(allow=['/tor/\d+']), callback='parse_torrent', follow=False)]

    def parse_torrent(self, response):
        torrent = TorrentItem()
        torrent['url'] = response.url
        torrent['name'] = response.xpath("//div[@id='content']/h1/text()").extract()
        torrent['desc'] = response.xpath("//div[@id='description']/text()").extract()
        torrent['size'] = response.xpath("//div[@id='specifications']/p[2]/text()").extract()
        return torrent
