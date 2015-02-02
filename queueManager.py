from multiprocessing.managers import BaseManager
from multiprocessing import Queue

"""
use python Queue in multiprocessing is easy to get a deadlock due to its implementation
but queue created using a manager does not have this issue
"""

class QueueManager(BaseManager):
    pass

queue = Queue()
QueueManager.register('Queue', lambda: queue)
mgr = QueueManager(address=('',12345), authkey='bilintechnology')
server = mgr.get_server()
server.serve_forever()
