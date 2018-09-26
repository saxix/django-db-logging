import json

import pytest
from django.urls import reverse

from django_db_logging.models import Record


@pytest.fixture(autouse=True)
def log1(db):
    return Record.objects.create(message='test-line1',
                                        extra=json.dumps({"a": 1}))

@pytest.fixture(autouse=True)
def log2(db):
    return Record.objects.create(message='test-line2', extra=None)



def test_admin(django_app, admin_user):
    url = reverse("admin:django_db_logging_record_changelist")
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200


def test_admin_detail(django_app, admin_user, log1, log2):
    url = reverse("admin:django_db_logging_record_change", args=[log1.pk])
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200

    url = reverse("admin:django_db_logging_record_change", args=[log2.pk])
    res = django_app.get(url, user=admin_user)
    assert res.status_code == 200


def test_admin_buttons_test(django_app, admin_user):
    url = reverse("admin:django_db_logging_record_changelist")
    res = django_app.get(url, user=admin_user)
    res = res.click("Test").follow()
    assert res.status_code == 200


def test_admin_buttons_empty(django_app, admin_user):
    url = reverse("admin:django_db_logging_record_changelist")
    res = django_app.get(url, user=admin_user)
    res = res.click("Empty Log")
    res = res.form.submit().follow()
    assert res.status_code == 200


def test_admin_buttons_cleanup(django_app, admin_user):
    url = reverse("admin:django_db_logging_record_changelist")
    res = django_app.get(url, user=admin_user)
    res = res.click("Cleanup").follow()
    assert res.status_code == 200
