import pytest

from schemas.base_schemas import ServiceType
from support.builders.search_query_builder import Condition, Op
from support.helpers.api.search_api_helper import SearchHelper

@pytest.fixture
def search_for_permissions(search_helper: SearchHelper, agg_collector_name, common_conditions_with_name):
    def _search_for_permissions(permission_name):
        permission_condition = Condition(field="osPermission", op=Op.EQUAL, value=permission_name)
        conditions = common_conditions_with_name + [permission_condition]
        return search_helper.search(agg_collector_name, *conditions)

    return _search_for_permissions

@pytest.mark.parametrize(
    'as_id, service_type, permission_name, title',
    [
        (111, ServiceType.FILESYS, '/root', "Permissions with FileSystem connector."),
        (222, ServiceType.AWS, '/aws-staging', "Permissions with AWS connector."),
        (333, ServiceType.SMB, 'Unix Group/root', "Permissions with SMB connector.")
    ])
def test_permissions_positive(as_id, service_type, permission_name, title, search_for_permissions, initial_scan_data):
    # Arrange
    scanned_file_name = initial_scan_data[service_type].get("file_name")
    # Action
    search_data = search_for_permissions(permission_name)

    # Assertion
    found_objects = search_data['objects']
    assert len(found_objects) == 1
    found_object = found_objects[0]
    assert found_object['name'] == scanned_file_name

@pytest.mark.parametrize(
    'as_id, service_type, permission_name, title',
    [
        (111, ServiceType.FILESYS, '/Everyone', "Permissions with FileSystem connector."),
        (222, ServiceType.AWS, 'Unix Group/root', "Permissions with AWS connector."),
        (333, ServiceType.SMB, '/root', "Permissions with SMB connector.")
    ])
def test_permissions_for_wrong_permissions(as_id, service_type, permission_name, title, search_for_permissions):
    # Action
    search_data = search_for_permissions(permission_name)

    # Assertion
    found_objects = search_data['objects']
    assert len(found_objects) == 0