"""
settings for set up context engine
"""

# path that store url list files
URL_LIST_PATH = '/tmp/urls/'

# url size of one spider, means one spider crawl URL_SIZE page total
# it also limits the size of each value in Queue
# default to 1000
URL_SIZE = 100

# spider number run at one time
# when use process pool, it's the pool size,
# when use single process, it's the spider count of single process
SPIDER_COUNT = 4

# Manager proxy ip, port and authkey
PROXY_IP = 'localhost'
PROXY_PORT = 12345
PROXY_AUTH = 'bilintechnology'

# proxy queue's size, set to zero or None means infinite
QUEUE_SIZE = 1000
