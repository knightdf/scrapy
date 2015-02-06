from multiprocessing.managers import BaseManager
import time
import os
import re
import settings

class MyManager(BaseManager):
    pass

MyManager.register('Queue')

class UrlReader():
    """
    read urls to Queue
    Note that it will move files that has been read to 'done' directory
    """

    def __init__(self, path, url_size=1000):
        """
        path is url files path
        url_size is the size of one url_list in Queue
        queue is a proxy object of remote manager
        """
        self._path = path
        self._url_size = url_size
        mgr = MyManager(address=(settings.PROXY_IP, settings.PROXY_PORT), authkey=settings.PROXY_AUTH)
        server = mgr.connect()
        self._queue = mgr.Queue()

    def decorate(self, url):
        """
        remove blanks in urls
        """
        m = re.match(r'.*(https?://\S+)\s?.*', url)
        return m and m.group(1)

    def readLines(self):
        """
        a generator return @self._url_size lines from @self._path every time
        """

        if self._path is not None and os.path.exists(self._path):
            res = []
            # the given path is a url list file
            if os.path.isfile(self._path):
                for line in open(self._path, 'r'):
                    line = self.decorate(line)
                    if line is not None:
                        res.append(line)
                    # return self._url_size lines
                    if len(res) >= self._url_size:
                        yield res
                        res = []
                # return the remaining lines
                if len(res) > 0:
                    yield res
                # move files that has been read to 'done' directory
                done_path = os.path.dirname(self._path)+os.path.sep+ 'done' +os.path.sep
                os.path.exists(done_path) or os.mkdir(done_path)
                os.rename(self._path, done_path+os.path.basename(self._path))
            # the given path is a dir including multi url_list
            elif os.path.isdir(self._path):
                for f in os.listdir(self._path):
                    filepath = os.path.join(self._path, f)
                    if os.path.isfile(filepath):
                        for line in open(filepath, 'r'):
                            line = self.decorate(line)
                            if line is not None:
                                res.append(line)
                            # return self._url_size lines
                            if len(res) >= self._url_size:
                                yield res
                                res = []
                        # return the remaining lines
                        if len(res) > 0:
                            yield res
                        # move files that has been read to 'done' directory
                        done_path = os.path.dirname(filepath)+os.path.sep+ 'done' +os.path.sep
                        os.path.exists(done_path) or os.mkdir(done_path)
                        os.rename(filepath, done_path+os.path.basename(filepath))
        else:
            raise IOError('url list path not found!')

    def toQueue(self):
        """
        put data to self._queue
        """

        f = self.readLines()
        while True:
            # wait until Queue is not full
            while self._queue.full():
                time.sleep(5)
            try:
                self._queue.put(f.next())
            except StopIteration:
                print('finished all files')
                break

if __name__ == '__main__':
    reader = UrlReader(path=settings.URL_LIST_PATH, url_size=settings.URL_SIZE)
    reader.toQueue()
