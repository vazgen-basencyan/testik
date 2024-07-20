from schemas.base_schemas import StatusEnum
from schemas.public_api_schemas.forgot_credentials_apis import ForgotCredentialsApiResponse
from support.utils.validation_util import Validator
from swagger_client import ForgotPasswordRequestBody

def test_server_api_v3_forgot_password(configs, public_api_instance):
    # response is always OK. Email is sent, but we cannot check it
    forgot_password_data = ForgotPasswordRequestBody(user_id=configs.autotest_password)
    api_response = public_api_instance.database_forgot_password_post(
        forgot_password_data=forgot_password_data)
    Validator(api_response).validate_status(StatusEnum.OK).validate_schema(ForgotCredentialsApiResponse)

def test_server_api_v3_forgot_userid(configs, public_api_instance):
    # response is always OK. Email is sent, but we cannot check it
    forgot_user_id_data = {'phoneOrEmail': configs.autotest_email}
    api_response = public_api_instance.database_forgot_user_id_post(
        forgot_user_id_data=forgot_user_id_data)
    Validator(api_response).validate_status(StatusEnum.OK).validate_schema(ForgotCredentialsApiResponse)