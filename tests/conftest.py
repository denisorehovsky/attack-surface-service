from rest_framework.test import APIClient
from fakeredis import FakeRedis
import pytest


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def fake_redis(mocker):
    fake_redis = FakeRedis()
    return fake_redis
