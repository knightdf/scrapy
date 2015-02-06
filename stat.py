from multiprocessing.managers import BaseManager
import settings

"""
show Queue stat
"""

class MyManager(BaseManager):
    pass

MyManager.register('Queue')

def run():
    mgr = MyManager(address=(settings.PROXY_IP, settings.PROXY_PORT), authkey=settings.PROXY_AUTH)
    server = mgr.connect()
    q = mgr.Queue()
    print('Queue size: %s'%q.qsize())

run()
