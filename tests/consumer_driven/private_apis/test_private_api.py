import pytest

from schemas.base_schemas import StatusEnum, ApiError
from schemas.base_schemas import CommonStatusResponse
from support.fixtures.setup_fixtures import get_current_environment
from support.utils.validation_util import Validator
from swagger_client import ActivateObject
OBJECTS = ['Admin', 'Everyone']


@pytest.mark.parametrize('activation_code', ['ACPFL-YLSZU-JZMMB-NVR7S'])
@pytest.mark.skipif(get_current_environment() != 'local', reason="Test is only for local environment")
def test_server_api_v3_database_activate_negative(public_api_instance_hybrid, private_api_instance,
                                                  activation_code):
    api_response_node = public_api_instance_hybrid.config_get()
    activate_object_body = ActivateObject(
        activation_code=activation_code,
        parent_id=api_response_node['data']['node']['parentNodeId']
    )
    api_response_platform = private_api_instance.database_activate_post(activate_object_body=activate_object_body)

    Validator(api_response_platform).validate_status(StatusEnum.error).validate_schema(ApiError)

    assert api_response_platform.get('message') == f'The activation code "{activation_code}" is not a valid ' \
                                                   f'activation code'

def test_update(private_api_instance):
    # PID_TRUSTEES | User and group objects that have permissions assigned to the object
    api_response = private_api_instance.update_get()
    Validator(api_response).validate_status(StatusEnum.OK).validate_schema(CommonStatusResponse)
