import pytest

from schemas.base_schemas import ServiceType
from support.builders.search_query_builder import Condition, Op
from support.helpers.api.search_api_helper import SearchHelper


@pytest.mark.parametrize(
    'as_id, service_type, title',
    [
        (111, ServiceType.FILESYS, "Core scan with file system connector."),
        (222, ServiceType.AWS, "Core scan with AWS connector."),
        (333, ServiceType.SMB, "Core scan with SMB connector."),
        (444, ServiceType.OBJSTORE, "Core scan with S3 compatible(Minio) connector."),
    ])
def test_core_scan(as_id, service_type: ServiceType, title, search_helper: SearchHelper, agg_collector_name, initial_scan_data):
    # Arrange
    scanned_file_name = initial_scan_data[service_type].get("file_name")
    name_specific_condition = Condition(field="name",op=Op.EQUAL,value=scanned_file_name)

    # Action
    search_data = search_helper.search(agg_collector_name, name_specific_condition)

    # Assertion
    found_objects = search_data['objects']
    assert len(found_objects) == 1
    found_object = found_objects[0]
    assert found_object['name'] == scanned_file_name
