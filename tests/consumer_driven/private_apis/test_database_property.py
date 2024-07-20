from __future__ import absolute_import

import pytest

from schemas.base_schemas import StatusEnum
from schemas.private_api_schemas.property_api import PropertyResponse
from support.utils.validation_util import Validator
from swagger_client import Object, PropertyId, CreatePropertyRequestBody, CreateObjectRequestBody

OBJECTS = ['Admin', 'Everyone']


@pytest.fixture(scope="function")
def setup_property_data(private_api_instance, home_id):
    new_role = Object(
        parent_id=home_id,
        name='test_role',
        class_id='group',
        tags={},
        properties={}
    )
    create_object_body = CreateObjectRequestBody(
        object=new_role,
        options={}
    )
    api_response = private_api_instance.database_object_post(create_object_body=create_object_body)

    object_id = api_response.get('data').get('objectId')
    create_property_body = CreatePropertyRequestBody(
        object_id=object_id,
        property_id=PropertyId.MEMBERS,
        _property=[],
        options={}
    )

    yield create_property_body

    private_api_instance.database_object_delete(object_id=object_id, options='{"infoLevel":"full"}')


def test_database_property_get(private_api_instance, home_id):
    # PID_TRUSTEES | User and group objects that have permissions assigned to the object
    api_response = private_api_instance.database_property_get(object_id=home_id,
                                                              property_id=PropertyId.TRUSTEES,
                                                              options='{"infoLevel":"full"}')
    api_data = api_response.get('data')

    Validator(api_response).validate_status(StatusEnum.OK).validate_schema(PropertyResponse)

    assert [api_data[i].get('object')['parentId'] == home_id for i in
            range(len(api_data))], "Object_id is a parent_id for users and groups objects"
    assert any(role in [api_data[i].get('object')['uniqueName'] for i in
                        range(len(api_data))] for role in
               OBJECTS), f"Users and groups names for the object are {OBJECTS}"


def test_database_property_post(private_api_instance, setup_property_data):
    create_property_body = setup_property_data
    property_post_response = private_api_instance.database_property_post(create_property_body=create_property_body)

    Validator(property_post_response).validate_status(StatusEnum.OK).validate_schema(PropertyResponse)

    property_get_response = private_api_instance.database_property_get(
        object_id=create_property_body.object_id,
        property_id=PropertyId.MEMBERS,
        options='{"infoLevel":"full"}'
    )

    Validator(property_get_response).validate_status(StatusEnum.OK).validate_schema(PropertyResponse)
