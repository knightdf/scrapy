# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from datetime import datetime
from elasticsearch import Elasticsearch
from scrapy import log
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings
from hashlib import md5

class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item

class TorrentPipeline(object):
    def __init__(self):
        self.index_name = 'mininova'
        self.doc_type = 'torrent'
        self.es = Elasticsearch(settings.getlist('ES_HOST'))
        self.es.indices.create(index=self.index_name, ignore=400)

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
        res = self.es.index(
                index=self.index_name,
                doc_type=self.doc_type,
                id=item['url'].split('/')[-1],
                body=doc
            )
        self.es.indices.refresh(index=self.index_name)
        log.msg(res['created'], level=log.INFO)
        return item

    def close_spider(self, spider):
        self.es.indices.refresh(index=self.index_name)

class BroadPipeline(object):
    def __init__(self):
        self.index_name = 'bilintest'
        self.doc_type = 'page'
        settings = get_project_settings()
        self.es = Elasticsearch(settings.getlist('ES_HOST'))

        mapping = {
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
                        'timestamp': {
                            'type': 'date',
                            },
                        'keywords': {
                            'type': 'string',
                            'store': True,
                            'index': 'analyzed'
                            }
                        }
                    }
                }

        self.es.indices.create(index=self.index_name, ignore=400)

    def process_item(self, item, spider):
        if spider.name != 'broad':
            return item
        try:
            if not (item['body'] and item['url']):
                raise DropItem('missing content or url in %s'%item)
        except:
            raise DropItem('missing url or content in %s'%item)

        doc = {
                'title': item['title'],
                'url': item['url'],
                'content': item['body'],
                'keywords': item['keywords'],
                'timestamp': datetime.utcnow()
                }

        res = self.es.index(
                index=self.index_name,
                doc_type = self.doc_type,
                id = md5(item['url']).hexdigest(),
                body = doc
                )

        return item
