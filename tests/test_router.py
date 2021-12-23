from django.contrib.auth.models import User

from django_db_logging.models import Record
from django_db_logging.router import LoggingRouter


def test_router():
    ALIAS = "logging"
    router = LoggingRouter(ALIAS)
    assert router.db_for_read(Record) == ALIAS
    assert router.db_for_write(Record) == ALIAS
    assert router.allow_migrate(ALIAS, 'django_db_logging')

    assert router.db_for_read(User) is None
    assert router.allow_migrate('default', 'auth') is None
