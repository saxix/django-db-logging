import logging

from demo.models import CustomLogger


def test_custom_record(db):
    logger = logging.getLogger('demo')
    logger.info('custom log')

    assert CustomLogger.objects.filter(level=logging.INFO,
                                       message='custom log').exists()
