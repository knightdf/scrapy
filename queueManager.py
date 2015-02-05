from multiprocessing.managers import BaseManager
from multiprocessing import Queue
import settings

"""
use python Queue in multiprocessing is easy to get a deadlock due to its implementation
but queue created using a manager does not have this issue
"""

class QueueManager(BaseManager):
    pass

queue = Queue(settings.QUEUE_SIZE)
QueueManager.register('Queue', lambda: queue)
mgr = QueueManager(address=('',settings.PROXY_PORT), authkey=settings.PROXY_AUTH)
server = mgr.get_server()
server.serve_forever()
