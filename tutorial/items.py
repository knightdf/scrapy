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

class BroadItem(scrapy.Item):
    title = scrapy.Field()
    keywords = scrapy.Field()
    url = scrapy.Field()
    body = scrapy.Field()

    def __getitem__(self, key):
        try:
            return super(BroadItem, self).__getitem__(key)
        except KeyError:
            return None
