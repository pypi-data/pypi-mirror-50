__version__ = '0.1.8'
__author__ = 'fx-kirin <fx.kirin@gmail.com>'
__all__ = ['Lock']

"""
Thread-safe lock mechanism with timeout support module.
"""

import traceback
from queue import Empty, Full, Queue
from threading import ThreadError, current_thread

import kanilog

logger = kanilog.get_module_logger(__file__, 1)


class Lock(object):
    """
    Thread-safe lock mechanism with timeout support.
    """

    def __init__(self, timeout=None):
        self._queue = Queue(maxsize=1)
        self._owner = None
        if timeout:
            self._timeout = timeout
        else:
            self._timeout = 0

    def acquire(self, timeout=None):
        if timeout:
            timeout = self._timeout
        th = current_thread()
        trace = traceback.extract_stack()
        try:
            logger.debug('Acquiring Lock:%s', trace[-3])
            self._queue.put(
                th, block=(timeout != 0),
                timeout=(None if timeout < 0 else timeout)
            )
            logger.debug('Acquired Lock:%s', trace[-3])
        except Full:
            logger.error('Timeout from acquiring Lock:%s', trace[-3])
            raise ThreadError('Lock Timed Out')

        self._owner = th
        return True

    def release(self):
        th = current_thread()
        if th != self._owner:
            raise ThreadError('This lock isn\'t owned by this thread.')

        self._owner = None
        try:
            trace = traceback.extract_stack()
            logger.debug('releasing Lock:%s', trace[-3])
            self._queue.get(False)
            return True
        except Empty:
            raise ThreadError('This lock was released already.')

    def __enter__(self, *args, **kwargs):
        if 'timeout' in kwargs:
            self.acquire(timeout=kwargs['timeout'])
        else:
            self.acquire(self._timeout)

    def __exit__(self, *args, **kwargs):
        self.release()
