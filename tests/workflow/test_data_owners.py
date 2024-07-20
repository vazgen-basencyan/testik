import pytest

from schemas.base_schemas import ServiceType
from support.builders.search_query_builder import Condition, Op
from support.helpers.api.search_api_helper import SearchHelper

@pytest.fixture
def search_for_data_owners(search_helper: SearchHelper, agg_collector_name, common_conditions_with_name):
    def _search_for_data_owners(data_owner_name):
        permission_condition = Condition(field="osOwner", op=Op.EQUAL, value=data_owner_name)
        conditions = common_conditions_with_name + [permission_condition]
        return search_helper.search(agg_collector_name, *conditions)

    return _search_for_data_owners

@pytest.mark.parametrize(
    'as_id, service_type, data_owner_name, title',
    [
        (111, ServiceType.FILESYS, '/root', "Data owners results with FileSystem connector."),
        (222, ServiceType.AWS, '/aws-staging', "Data owners results with AWS connector."),
        (333, ServiceType.SMB, 'Unix User/root', "Data owners results with SMB connector.")
    ])
def test_data_owners_positive(as_id, service_type, data_owner_name, title, search_for_data_owners, initial_scan_data):
    # Arrange
    scanned_file_name = initial_scan_data[service_type].get("file_name")
    # Action
    search_data = search_for_data_owners(data_owner_name)

    # Assertion
    found_objects = search_data['objects']
    assert len(found_objects) == 1
    found_object = found_objects[0]
    assert found_object['name'] == scanned_file_name

@pytest.mark.parametrize(
    'as_id, service_type, data_owner_name, title',
    [
        (111, ServiceType.FILESYS, '/Everyone', "Data owners results with FileSystem connector."),
        (222, ServiceType.AWS, 'Unix Group/root', "Data owners results with AWS connector."),
        (333, ServiceType.SMB, '/root', "Data owners results with SMB connector.")
    ])
def test_data_owners_for_wrong_permissions(as_id, service_type, data_owner_name, title, search_for_data_owners):
    # Action
    search_data = search_for_data_owners(data_owner_name)

    # Assertion
    found_objects = search_data['objects']
    assert len(found_objects) == 0