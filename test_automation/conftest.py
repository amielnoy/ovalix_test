import os
from dotenv import load_dotenv
import pytest

HERE = os.path.dirname(__file__)
load_dotenv(os.path.join(HERE, '.env'))
load_dotenv(os.path.join(HERE, '.env'))

from .http_client import HttpClient
from .services.user_service import UserService


@pytest.fixture(scope='session')
def http_client():
    base = os.getenv('API_BASE_URL')
    return HttpClient(base)


@pytest.fixture
def user_service(http_client):
    return UserService(http_client)
