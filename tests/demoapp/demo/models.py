from django_db_logging.models import AbstractRecord


class CustomLogger(AbstractRecord):
    class Meta:
        app_label = 'demo'
