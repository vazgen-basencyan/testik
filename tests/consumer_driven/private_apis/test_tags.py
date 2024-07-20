from __future__ import absolute_import

import pytest

from schemas.base_schemas import ServiceType
from schemas.base_schemas import StatusEnum
from schemas.base_schemas import CommonStatusResponse
from support.utils.validation_util import Validator
from swagger_client import TagsRequestBody
from support.builders.search_query_builder import Condition, Op
from support.helpers.api.search_api_helper import SearchHelper

OBJECTS = ['Admin', 'Everyone']


@pytest.fixture(scope="class")
def setup_tags(private_api_instance, home_id, search_helper: SearchHelper, agg_col_info, initial_scan_data):
    file_name_scanned_by_file_system = initial_scan_data[ServiceType.FILESYS].get("file_name")
    search_data = search_helper.search(agg_col_info['name'],
                                       Condition(field="name",
                                                 op=Op.EQUAL,
                                                 value=file_name_scanned_by_file_system))

    tag_definitions = ['test']
    tagDefBody = {"clientObjectId": home_id, "tagDefinitions": ["testik"]}
    # Create tag as test setup
    private_api_instance.tag_definitions_post(post_tag_definition_body=tagDefBody)
    instanceId = search_data['objects'][0]['instanceId']
    objectId = search_data['objects'][0]['objectId']
    objects = {"objectId": objectId, "instanceId": instanceId}
    create_property_body = TagsRequestBody(objects=[objects], tags=tag_definitions)
    yield create_property_body

    # Delete tag as test teardown
    private_api_instance.tags_delete(delete_tags_body=tagDefBody)


class TestTagsApi:
    def test_tags_post(self, private_api_instance, setup_tags):
        # Create tag
        api_response = private_api_instance.tags_post(post_tags_body=setup_tags)
        # Validate response
        Validator(api_response).validate_status(StatusEnum.OK).validate_schema(CommonStatusResponse)

    def test_tags_delete(self, private_api_instance, setup_tags):
        # Create tag
        private_api_instance.tags_post(post_tags_body=setup_tags)
        # Delete tag
        api_response = private_api_instance.tags_delete(delete_tags_body=setup_tags)
        # Validate response
        Validator(api_response).validate_status(StatusEnum.OK).validate_schema(CommonStatusResponse)
