import pytest

from schemas.base_schemas import StatusEnum
from schemas.public_api_schemas.auth_api import AuthApiResponse, AuthApiNegativeResponse
from support.utils.validation_util import Validator

@pytest.mark.parametrize("command", ['authentication.available'])
def test_server_api_v3_auth_get_positive(command, public_api_instance):
    api_response = public_api_instance.auth_get(command=command)
    Validator(api_response).validate_status(StatusEnum.OK).validate_schema(AuthApiResponse)

@pytest.mark.parametrize("command", ['authentication.unavailable'])
def test_server_api_v3_auth_get_negative(command, public_api_instance):
    api_response = public_api_instance.auth_get(command=command)
    Validator(api_response).validate_status(StatusEnum.error).validate_schema(AuthApiNegativeResponse)