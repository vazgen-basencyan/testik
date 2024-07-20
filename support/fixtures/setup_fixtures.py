import time
from urllib.parse import urljoin
import pytest

import swagger_client

from support.helpers.api.objects_api_helper import ObjectHelper
from support.setup_models.exceptions import NodeNotFoundException
from swagger_client import NodeId, PrivateApi, Configuration, PublicApi, LoginRequestBody, AuthProviderState
from schemas.base_schemas import SetupConfigs
from dotenv import load_dotenv
import os

load_dotenv()


@pytest.fixture(scope='session')
def agg_col_id(home_id, private_api_instance):
    """returns current's client node id"""
    agg_col_id = get_node(home_id, private_api_instance, NodeId.APPAGT)
    return agg_col_id.get('objectId')

def get_node(home_id: str, private_api_instance: PrivateApi, node_id: NodeId):
    response = private_api_instance.database_children_get(home_id)
    children_objects = response['data']['objects']
    filtered_nodes = [node for node in children_objects if node.get('classId') == node_id]
    if filtered_nodes:
        return filtered_nodes[0]
    else:
        raise NodeNotFoundException(f'Unable to find the node for class {node_id}.')


@pytest.fixture(scope="session")
def api_instance_configuration(configs) -> Configuration:
    configuration = swagger_client.Configuration()
    configuration.host = urljoin(configs.host, configs.base_path)
    return configuration


@pytest.fixture(scope="session")
def public_api_instance(api_instance_configuration) -> PublicApi:
    return swagger_client.PublicApi(swagger_client.ApiClient(api_instance_configuration))


@pytest.fixture(scope="session")
def public_api_instance_hybrid(configs: SetupConfigs) -> PublicApi:
    configuration = swagger_client.Configuration()
    configuration.host = f'{configs.host}:{configs.hybrid_port}{configs.base_path}'
    return swagger_client.PublicApi(swagger_client.ApiClient(configuration))


@pytest.fixture(scope="session")
def session_variables():
    return dict()


@pytest.fixture(scope="session")
def private_api_instance(api_instance_configuration, configs, public_api_instance, session_variables) -> PrivateApi:
    timestamp = time.time()
    command = 'authentication.available'
    api_auth_info_response = public_api_instance.auth_get(command=command)
    api_response = login(api_auth_info_response, configs, public_api_instance, timestamp)

    # Save homeId in the session scope
    configuration = prepare_configuration(api_instance_configuration, api_response, session_variables)

    return swagger_client.PrivateApi(swagger_client.ApiClient(configuration))


def prepare_configuration(api_instance_configuration, api_response, session_variables):
    api_data = api_response.get('data')
    session_variables['home_id'] = api_data.get('homeId')
    configuration = api_instance_configuration
    configuration.api_key['Authorization'] = api_data.get('token')
    return configuration


def login(api_auth_info_response, configs, public_api_instance, timestamp):
    state = AuthProviderState(
        provider="integrated",
        id=api_auth_info_response['data'][0]['state']['id'],
        client_object_id="",
        timestamp=timestamp
    )
    login_data = LoginRequestBody(
        user_id=configs.autotest_username,
        password=configs.autotest_password,
        provider="integrated",
        state=state
    )
    return public_api_instance.login_post(login_data=login_data)


@pytest.fixture(scope="session")
def home_id(private_api_instance, session_variables) -> str:
    return session_variables["home_id"]


@pytest.fixture(scope="session")
def agg_col_info(agg_col_id, private_api_instance):
    return ObjectHelper(private_client=private_api_instance).get_object(object_id=agg_col_id)


@pytest.fixture(scope="session")
def configs():
    return SetupConfigs(
        autotest_username=os.getenv("AUTOTEST_USERNAME"),
        autotest_password=os.getenv("AUTOTEST_PASSWORD"),
        autotest_email=os.getenv("AUTOTEST_EMAIL"),
        root_username=os.getenv("ROOT_USERNAME"),
        root_password=os.getenv("ROOT_PASSWORD"),
        host=os.getenv("HOST"),
        base_path=os.getenv("BASE_PATH"),
        hybrid_port=os.getenv("HYBRID_PORT"),
        version=os.getenv("VERSION"),
        scan_folder=os.getenv("SCAN_FOLDER")
    )


def get_current_environment():
    return os.environ.get('ENVIRONMENT', 'local')
