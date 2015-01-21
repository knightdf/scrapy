import random
import base64
from scrapy.exceptions import IgnoreRequest
from scrapy.utils.project import get_project_settings

class RandomUserAgent(object):
    """Random rotate user-agent based on a list of predefined ones"""

    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(self.agents))

class HttpProxy(object):
    def __init__(self):
        settings = get_project_settings()
        self.proxy_addr = settings.get('PROXY_ADDR')
        self.proxy_pass = settings.get('PROXY_PASS')

    def process_request(self, request, spider):
        if self.proxy_addr and self.proxy_pass:
            request.meta['proxy'] = self.proxy_addr
            request.headers['Proxy-Authorization'] = 'Basic '+ base64.encodestring(self.proxy_pass)
