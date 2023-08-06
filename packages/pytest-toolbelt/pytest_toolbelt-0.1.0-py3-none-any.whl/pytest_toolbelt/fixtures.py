import pytest

import requests

from pytest_toolbelt.utils import requests_retry_session

__all__ = [
    'requests_client'
]


@pytest.fixture()
def requests_client():
    class RequestsClient(requests.Session):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            requests_retry_session(
                retries=10,
                backoff_factor=1,
                status_forcelist=(500, 502, 504),
                session=self
            )

        def as_(self, user):
            self.headers['Authorization'] = f'Bearer {user["access_token"]}'
            return self

    return RequestsClient()
