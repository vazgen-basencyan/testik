import pytest

from support.helpers.api.scan_api_helpers import ScanHelper
from support.helpers.api.search_api_helper import SearchHelper


@pytest.fixture(scope="session")
def search_helper(private_api_instance) -> SearchHelper:
    yield SearchHelper(private_client=private_api_instance)


@pytest.fixture(scope="session")
def scan_helper(private_api_instance) -> ScanHelper:
    yield ScanHelper(private_client=private_api_instance)
