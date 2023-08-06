# -*- coding: utf-8 -*-
"""
Lock file
@author: fallthrough
"""
import threading
import time
from six.moves import queue


def make_timestamp_period(**kwargs):
    """
    convert time to timestamp
    :param kwargs: support minutes, seconds
    :return: timestamp
    """
    minutes = kwargs.get("minutes", 0)
    seconds = kwargs.get("seconds", 0)
    return minutes * 60 + seconds


class CountLock(object):
    """
    CountLock is a lock limited by time and count. It is recovered by periodicity.
    """

    def __init__(self, count, **kwargs):
        self._lock = threading.Lock()
        self._total_count = count
        self._queue = queue.Queue(count)
        self._current_count = 0
        self._last_modify_timestamp = 0
        self._restore_time_period = make_timestamp_period(**kwargs)

    def acquire(self):
        while True:
            self._acquire()
            try:
                self._queue.get(timeout=1)
            except queue.Empty:
                pass
            else:
                break

    def _acquire(self):
        current_timestamp = time.time()
        self._lock.acquire()
        if current_timestamp - self._last_modify_timestamp > self._restore_time_period:
            self._restore_count()
            self._last_modify_timestamp = current_timestamp
        self._lock.release()

    def _restore_count(self):
        for _ in range(self._total_count - self._queue.qsize()):
            self._queue.put(1)
