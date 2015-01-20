# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from exceptions import KeyError


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()

class TorrentItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    desc = scrapy.Field()
    size = scrapy.Field()

class NewsItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    time = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()
    _type = scrapy.Field()

class BBCItem(scrapy.Item):
    keywords = scrapy.Field()
    postId = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    time = scrapy.Field()
    url = scrapy.Field()
    channel = scrapy.Field()

    def __getitem__(self, key):
        try:
            super(BBCItem, self).__getitem__(key)
        except KeyError:
            return None

class BroadItem(scrapy.Item):
    title = scrapy.Field()
    keywords = scrapy.Field()
    url = scrapy.Field()
    body = scrapy.Field()
