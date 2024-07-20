import os
import shutil

import pytest

from schemas.base_schemas import ServiceType, SetupConfigs
from support.clients.aws_client import AWSClient
from support.clients.minio_client import MinioClient
from support.generator import create_temp_files
from support.helpers.api.scan_api_helpers import ScanHelper
from support.helpers.generic_helpers import get_file_name_from_path
import time


@pytest.fixture(scope="session")
def aws_client() -> AWSClient:
    aws_bucket = os.environ.get('AWS_BUCKET')
    return AWSClient(aws_bucket)


@pytest.fixture(scope="session")
def minio_client() -> MinioClient:
    minio_endpoint = os.environ.get('MINIO_ENDPOINT')
    access_key = os.environ.get('MINIO_ACCESS_KEY')
    secret_key = os.environ.get('MINIO_SECRET_KEY')
    return MinioClient(endpoint=minio_endpoint, access_key=access_key, secret_key=secret_key)


@pytest.fixture(scope="session")
def worker_id():
    return os.environ.get('PYTEST_XDIST_WORKER')


@pytest.fixture(scope="session")
def session_temp_files(request, configs: SetupConfigs, worker_id, aws_client: AWSClient, minio_client: MinioClient, num_files=3):
    if is_master_node(worker_id):
        files_paths = create_temp_files(configs, num_files)
        temp_data = prepare_temp_data(request, files_paths)

        aws_file_info = temp_data[ServiceType.AWS]
        aws_client.upload(aws_file_info["file_path"], aws_file_info["aws_object_for_upload"])

        s3_file_info = temp_data[ServiceType.OBJSTORE]
        minio_client.client.set_bucket_name(s3_file_info['s3_bucket'])
        minio_client.client.create_bucket()
        minio_client.client.upload(s3_file_info["file_path"], s3_file_info['file_name'])

        def finalizer():
            remove_temp_files(files_paths)
            aws_client.delete_folder(aws_file_info["aws_object_for_upload"])
            minio_client.client.remove_bucket()

        request.addfinalizer(finalizer)


def remove_temp_files(files_paths):
    for file_path in files_paths:
        if os.path.exists(file_path):
            try:
                file_dir = os.path.dirname(file_path)
                shutil.rmtree(file_dir)
            except FileNotFoundError:
                pass


@pytest.fixture(scope="session")
def initial_scan_data(request):
    return request.config.cache.get('initial_scan_data', default=None)


def prepare_temp_data(request, temp_files_paths):
    temp_files_info = {ServiceType.FILESYS: create_and_get_temp_file_info(temp_files_paths[0]),
                       ServiceType.AWS: create_and_get_aws_temp_file_info(temp_files_paths[1]),
                       ServiceType.SMB: create_and_get_smb_temp_file_info(),
                       ServiceType.OBJSTORE: create_and_get_s3_temp_file_info(temp_files_paths[2])}
    request.config.cache.set("initial_scan_data", temp_files_info)
    return temp_files_info


def create_and_get_s3_temp_file_info(temp_file_path):
    minio_temp_file_info = create_and_get_temp_file_info(temp_file_path)
    file_name = minio_temp_file_info['file_name']
    bucket_name = file_name.split(".")[0]
    minio_temp_file_info["s3_path"] = "{}/*".format(bucket_name)
    minio_temp_file_info["s3_bucket"] = bucket_name
    return minio_temp_file_info


def create_and_get_smb_temp_file_info():
    smb_share_name = os.environ.get('SMB_SHARE_NAME')
    smb_share_path = os.environ.get('SMB_PATH')
    smb_path = "{}{}".format(smb_share_name, smb_share_path)
    return {'file_name': 'include1.txt', 'smb_path': smb_path}


def create_and_get_aws_temp_file_info(temp_file_path):
    aws_temp_file_info = create_and_get_temp_file_info(temp_file_path)
    aws_bucket = os.environ.get('AWS_BUCKET')
    file_name = aws_temp_file_info['file_name']
    folder_name = file_name.split(".")[0]
    aws_temp_file_info["aws_object_for_upload"] = "{}/{}".format(folder_name, file_name)
    aws_temp_file_info["aws_path"] = "{}/{}/*".format(aws_bucket, folder_name)
    return aws_temp_file_info


def create_and_get_temp_file_info(temp_file_path):
    file_name = get_file_name_from_path(temp_file_path)
    return {'file_name': file_name, 'file_path': temp_file_path}


def create_lock_file(lock_path):
    open(lock_path, 'a').close()


def wait_for_lock_file(lock_path, max_wait_time=100, wait_interval=1):
    elapsed_time = 0
    while not lock_path.is_file() and elapsed_time < max_wait_time:
        time.sleep(wait_interval)
        elapsed_time += wait_interval


@pytest.fixture(scope="session", autouse=True)
def initial_scan(tmp_path_factory, agg_col_id, request, scan_helper: ScanHelper, worker_id, session_temp_files):
    TMP_ROOT = tmp_path_factory.getbasetemp().parent
    LOCK_PATH = TMP_ROOT / 'before_all.lock'

    ignore_scan = os.environ.get('IGNORE_INIT_SCAN')

    if ignore_scan != 'true':
        if is_master_node(worker_id):
            scan_helper.execute_core_scan(agg_col_id, request)
            create_lock_file(LOCK_PATH)
        else:
            wait_for_lock_file(LOCK_PATH)


def is_master_node(worker_id):
    return worker_id is None or worker_id == 'gw0'
