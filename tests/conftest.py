from django.test import TestCase


def pytest_configure(config):
    pass


TestCase.databases = {"default", "logging"}
