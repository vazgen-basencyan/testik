import pytest

from support.builders.search_query_builder import Condition, Op


@pytest.fixture
def common_conditions_with_name(initial_scan_data, service_type):
    scanned_file_name = initial_scan_data[service_type].get("file_name")
    return [Condition(field="name", op=Op.EQUAL, value=scanned_file_name)]