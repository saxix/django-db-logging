import logging
from unittest import mock

import pytest
from django_db_logging.handlers import DBHandler
from django_db_logging.models import Record


class DebugHandler(logging.Handler):
    records = []

    def emit(self, record):
        self.records.append(record)


@pytest.mark.django_db
def test_exception(db):
    Record.objects.all().delete()
    debugger = DebugHandler()
    logger = logging.getLogger('django_db_logging')

    logger.handlers = []
    logger.setLevel(logging.DEBUG)
    logger.addHandler(DBHandler())
    logger.addHandler(debugger)

    with mock.patch('django_db_logging.models.Record.objects.create',
                    side_effect=Exception("Database not ready")):
        logger.info("wally")

    assert logger.handlers == [debugger], logger.handlers
    assert len(debugger.records) == 2
    original_record = debugger.records[0]
    excp = debugger.records[1]
    assert original_record.levelno == logging.INFO
    assert original_record.msg == "wally"
    assert excp.levelno == logging.ERROR
    assert str(excp.msg) == "Database not ready"
    assert not Record.objects.filter(level=logging.ERROR).exists()
