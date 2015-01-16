from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from tutorial.items import NewsItem
import re

class NewsSpider(CrawlSpider):
    name = 'news'
    allowed_domains = ['163.com']
    start_urls = ['http://news.163.com/']
    rules = [Rule(SgmlLinkExtractor(allow=['/15/\d{4}/\d{2}/\w+\.html']), callback='parse_news', follow=True)]

    def parse_news(self, response):
        news = NewsItem()
        news['title'] = response.xpath("//*[@id='h1title']/text()").extract()
        contents = response.xpath("//*[@id='endText']/p")
        news['content'] = []
        for content in contents:
            news['content'].extend(content.xpath("text()|/strong/text()").extract())
        news['time'] = response.xpath("//*[@id='epContentLeft']/div[1]/div[1]/text()[1]").extract()
        m = re.match(r'(\d.+\d.*\d.+\d)', ((news['time'] and news['time'][0]) or '').strip())
        if m:
            news['time'] = m.group(1)
        else:
            news['time'] = ((news['time'] and news['time'][0]) or '').strip()
        news['source'] = response.xpath("//*[@id='ne_article_source']/text()").extract()
        news['url'] = response.url
        m = re.match(r'^http://(\w+)\.',response.url)
        if m:
            news['_type'] = m.group(1)
        else:
            news['_type'] = 'news'
        return news
