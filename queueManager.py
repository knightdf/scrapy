from multiprocessing.managers import BaseManager
from multiprocessing import Queue

class QueueManager(BaseManager):
    pass

queue = Queue()
QueueManager.register('Queue', lambda: queue)
mgr = QueueManager(address=('',12345), authkey='bilintechnology')
server = mgr.get_server()
server.serve_forever()
