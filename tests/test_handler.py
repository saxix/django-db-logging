import logging
import sys
import types
from time import sleep
from unittest.mock import Mock

import pytest
from django_db_logging.settings import config
from django_db_logging.handlers import AsyncDBHandler, DBHandler
from django_db_logging.models import Record

logger = logging.getLogger('test')
logger.setLevel(logging.DEBUG)


@pytest.mark.parametrize("level,expected", [("info", logging.INFO),
                                            ("error", logging.ERROR),
                                            ("debug", logging.DEBUG),
                                            ("warning", logging.WARN),
                                            ("critical", logging.CRITICAL),
                                            ("exception", logging.ERROR)])
@pytest.mark.parametrize("handler", [DBHandler, AsyncDBHandler])
def test_handlers(db, handler, level, expected):
    for hdlr in logger.handlers[:]:  # remove all old handlers
        logger.removeHandler(hdlr)
    logger.addHandler(handler())

    getattr(logger, level)(f'test-info {level} - {DBHandler}')
    if handler == AsyncDBHandler:
        sleep(1)

    log = Record.objects.latest()
    assert log.level == expected, log
    assert log.logger == 'test'


@pytest.mark.parametrize("handler", [DBHandler, AsyncDBHandler])
def test_handlers_exception(db, handler):
    logger.addHandler(handler())

    try:
        raise Exception("test")
    except Exception as e:
        logger.exception(e)

    if handler == AsyncDBHandler:
        sleep(2)

    log = Record.objects.latest()
    assert str(log)
    assert log.level == logging.ERROR
    assert log.logger == 'test'


def test_crashlog(db, monkeypatch):
    monkeypatch.setattr(config, 'USE_CRASHLOG', True)

    module_name = 'crashlog.middleware'
    bogus_module = types.ModuleType(module_name)
    sys.modules[module_name] = bogus_module
    bogus_module.process_exception = Mock(name=module_name + '.process_exception')

    for hdlr in logger.handlers[:]:  # remove all old handlers
        logger.removeHandler(hdlr)

    logger.addHandler(DBHandler())

    try:
        raise Exception("test")
    except Exception as e:
        logger.exception(e)

    log = Record.objects.latest()
    assert log.level == logging.ERROR
    assert log.logger == 'test'
    assert bogus_module.process_exception.call_count == 1
