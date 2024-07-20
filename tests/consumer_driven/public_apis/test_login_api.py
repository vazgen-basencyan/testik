import time

import pytest

from schemas.base_schemas import StatusEnum
from schemas.public_api_schemas.login_api import LoginResponse, LoginNegativeResponse
from support.generator import generate_random_string, generate_random_password
from support.utils.validation_util import Validator
from swagger_client import AuthProviderState, LoginRequestBody

list_error_codes_and_messages = {
    'AccountLoginFailure': 'The account does not exist or the incorrect password was specified'
}

def test_server_api_v3_login_post_positive(configs, public_api_instance):
    username = configs.autotest_username
    timestamp = time.time()
    state = AuthProviderState(provider="integrated", id="", client_object_id="", timestamp=timestamp)
    login_data = LoginRequestBody(user_id=username, password=configs.autotest_password,
                                  provider="integrated", state=state)

    api_response = public_api_instance.login_post(login_data=login_data)
    Validator(api_response).validate_status(StatusEnum.OK).validate_schema(LoginResponse)

    api_data = api_response.get('data')
    assert api_data.get('userId') == username, f"The userId should be '{username}'"
    assert api_data.get('name') == username, f"The name should be '{username}'"


@pytest.mark.parametrize(
    'as_id, user_id, password, expected_status, title',
    [
        (25527, generate_random_string(), generate_random_password(), StatusEnum.error,
         "Negative case: incorrect account name and password"),
        (25528, "", generate_random_password(), StatusEnum.error,
         "Negative case: incorrect password, but correct account name"),
        (25529, generate_random_string(), "", StatusEnum.error,
         "Negative case: incorrect account name, but correct password"),
        (25530, None, None, StatusEnum.error, "Negative case: Log in via null credentials")
    ])
def test_server_api_v3_login_post_negative(as_id, user_id, password, expected_status, title, public_api_instance,
                                           configs):
    if user_id == "":
        user_id = configs.autotest_username
    password = password or configs.autotest_password
    timestamp = time.time()
    state = AuthProviderState(provider="integrated", id="", client_object_id="", timestamp=timestamp)
    login_data = LoginRequestBody(user_id=user_id, password=password, provider="integrated", state=state)

    api_response = public_api_instance.login_post(login_data=login_data)

    Validator(api_response).validate_status(expected_status).validate_schema(LoginNegativeResponse)

    assert api_response.get('name') == 'AccountLoginFailure', "API response name should be 'AccountLoginFailure'"
    assert api_response.get('message') == list_error_codes_and_messages['AccountLoginFailure'], \
        "API response message should be '{list_error_codes_and_messages['AccountLoginFailure']}'"
