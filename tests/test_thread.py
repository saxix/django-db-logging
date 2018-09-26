# -*- coding: utf-8 -*-
import logging
from time import sleep
from unittest.mock import Mock

from django_db_logging.threadqueue import ThreadQueue

logger = logging.getLogger(__name__)


class Logger(ThreadQueue):
    TOTAL = 0

    def _process(self, record):
        self.TOTAL += sum(record)


def test_async():
    logger = Logger(shutdown_timeout=2)
    logger.queue([1, 1, 1])
    logger.queue(Logger._terminator)
    logger.start()
    sleep(1)
    logger.stop()
    assert logger.TOTAL == 3


def test_async_main_thread_terminated():
    logger = Logger(shutdown_timeout=2)
    logger.queue([1, 1, 1])
    logger.queue([1, 1, 1])
    logger.queue([1, 1, 1])
    logger.queue([1, 1, 1])
    logger.start()
    logger.main_thread_terminated()
    assert logger.TOTAL == 12


def test_async_timeout(monkeypatch):
    monkeypatch.setattr(ThreadQueue, '_timed_queue_join', lambda *args: False)
    # monkeypatch.setattr(AsyncQueue, '_async_timeout', lambda *args: True)

    logger = Logger(shutdown_timeout=0.001)
    logger.queue([1, 1, 1])
    sleep(2)
    logger.queue([1, 1, 1])
    logger.queue([1, 1, 1])
    logger.queue([1, 1, 1])
    sleep(2)
    logger.main_thread_terminated()
    assert logger.TOTAL == 12


def test_async_missing_start(monkeypatch):
    monkeypatch.setattr(ThreadQueue, 'start', lambda s: False)

    logger = Logger()
    logger.stop()
    assert logger.TOTAL == 0


def test_missing_thread(monkeypatch):
    monkeypatch.setattr(ThreadQueue, 'start', lambda s: True)
    logger = Logger()
    logger.queue([1, 1, 1])
    logger.stop()
    assert logger.TOTAL == 0


def test_async__timed_queue_join(monkeypatch):
    logger = Logger()
    monkeypatch.setattr(logger, '_queue', Mock(all_tasks_done=Mock(), unfinished_tasks=True), raising=False)

    assert not logger._timed_queue_join(1)
