from __future__ import absolute_import

import pytest
from support.fixtures.setup_fixtures import get_current_environment
from support.utils.validation_util import Validator
from schemas.public_api_schemas.changelog_api import ChangeLogApiResponse
from schemas.public_api_schemas.config_api import ConfigApiResponse
from schemas.public_api_schemas.forgot_credentials_apis import ForgotCredentialsApiResponse
from schemas.public_api_schemas.metrics_api import MetricsApiNegativeResponse, MetricsApiPositiveResponse
from schemas.base_schemas import StatusEnum, StringResponse

def test_server_api_v3_config(public_api_instance):
    api_response = public_api_instance.config_get()
    Validator(api_response).validate_status(StatusEnum.OK).validate_schema(ConfigApiResponse)

def test_server_api_v3_changelog(public_api_instance):
    api_response = public_api_instance.changelog_get()
    Validator(api_response).validate_status(StatusEnum.OK).validate_schema(ChangeLogApiResponse)

def test_server_api_v3_docs(public_api_instance):
    api_response = public_api_instance.docs_get()
    Validator(api_response).validate_schema(StringResponse)

def test_server_api_v3_metrics(public_api_instance):
    api_response = public_api_instance.metrics_get()
    validator = Validator(api_response)
    if get_current_environment() == 'nomad':
        validator.validate_schema(MetricsApiPositiveResponse)
    else:
        validator.validate_status(StatusEnum.error).validate_schema(MetricsApiNegativeResponse)


@pytest.mark.skip(reason="timout error")
def test_server_api_v3_listen_events(public_api_instance):
    api_response = public_api_instance.events_listen_get()
    Validator(api_response).validate_status(StatusEnum.OK).validate_schema(ForgotCredentialsApiResponse)

