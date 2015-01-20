# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime
from elasticsearch import Elasticsearch
from scrapy import log
from scrapy.exceptions import DropItem

class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item

class TorrentPipeline(object):
    def process_item(self, item, spider):
        if spider.name != 'torrents':
            return item
        doc = {
                'name': item['name'],
                'url': item['url'],
                'size': item['size'],
                'desc': item['desc'],
                'timestamp': datetime.utcnow()
            }
        es = Elasticsearch([
                {'host':'222.73.215.251', 'port':9200},
                {'host':'222.73.215.220', 'port':9200},
            ])
        es.indices.create(index='mininova', ignore=400)
        res = es.index(
                index='mininova',
                doc_type='link',
                id=item['url'].split('/')[-1],
                body=doc
            )
        es.indices.refresh(index='mininova')
        log.msg(res['created'], level=log.INFO)
        return item

class NewsPipeline(object):
    def __init__(self):
        self.index_name = 'newsof2015'
        self.es = Elasticsearch([
                {'host':'222.73.215.251', 'port':9200},
                {'host':'222.73.215.220', 'port':9200},
            ])
        self.es.indices.create(index=self.index_name, ignore=400)

    def process_item(self, item, spider):
        if spider.name != 'news':
            return item
        if not (item['title'] and item['content']):
            raise DropItem('missing title or content in %s'%item)

        doc = {
                'title': item['title'] and item['title'][0] or '',
                'url': item['url'],
                'content': self.get_content(item),
                'posttime': item['time'],
                'source': item['source'] and item['source'][0] or '',
                'type': item['_type'],
                'timestamp': datetime.utcnow()
            }
        res = self.es.index(
                index=self.index_name,
                doc_type=item['_type'] or 'news',
                id=item['url'].split('/')[-1].split('.')[0],
                body=doc
            )
        self.es.indices.refresh(index=self.index_name)
        log.msg(res['created'], level=log.INFO)
        return item

    def get_content(self, item):
        contents = ''
        for content in item['content']:
            contents += (content and content + '\r\n') or ''
        return contents

class BBCPipeline(object):
    def __init__(self):
        self.index_name = 'bbcnews'
        self.es = Elasticsearch([
                {'host':'222.73.215.251', 'port':9200}
            ])
        mapping = {
                'mappings':{
                    self.index_name: {
                        'properties': {
                            'title': {
                                'type': 'string',
                                'store': True,
                                'index': 'analyzed'
                                },
                            'url': {
                                'type': 'string',
                                'store': True
                                },
                            'content': {
                                'type': 'string',
                                'store': True,
                                'index': 'analyzed'
                                },
                            'posttime': {
                                'type': 'string',
                                'null_value': ''
                                },
                            'postid': {
                                'type': 'integer',
                                'null_value': ''
                                },
                            'type': {
                                'type': 'string',
                                },
                            'timestamp': {
                                'type': 'date',
                                },
                            'keywords': {
                                'type': 'string',
                                'store': True,
                                'index': 'analyzed',
                                'null_value': ''
                                }
                            }
                        }
                    }
                }

        self.es.indices.create(index=self.index_name, body=mapping, ignore=400)

    def process_item(self, item, spider):
        if spider.name != 'bbc':
            return item
        try:
            if not (item['postId'] and item['channel'] and item['title'] and item['content']):
                raise DropItem('missing title or content in %s'%item)
        except:
            raise DropItem('missing title or content in %s'%item)

        doc = {
                'title': item['title'],
                'url': item['url'],
                'content': item['content'],
                'posttime': item['time'],
                'postid': item['postId'],
                'type': item['channel'],
                'keywords': item['keywords'],
                'timestamp': datetime.utcnow()
                }

        res = self.es.index(
                index=self.index_name,
                doc_type = item['channel'],
                id = item['postId'],
                body = doc
                )

        return item

    def close_spider(self, spider):
        self.es.indices.refresh(index=self.index_name)
