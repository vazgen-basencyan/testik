import pytest


@pytest.fixture
def agg_collector_name(agg_col_info):
    return agg_col_info['name']