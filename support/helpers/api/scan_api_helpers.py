import os
import time
from support.constants import WAITING_COUNT, POLLING_TIME, START_WAITING_TIME
from support.helpers.api.base_api_helper import BaseHelper
from swagger_client import PropertyId, ControlCommandRequestBody, CommandId, \
    SourceParameters, ServiceIncludeData, ServiceObject, ModeType, CreatePropertyRequestBody
from schemas.base_schemas import StatusEnum, ServiceType


def set_inherited_as_false(agg_col_source_property):
    agg_col_source_property['rootSettings']['inherited'] = False
    agg_col_source_property['encryption']['inherited'] = False
    agg_col_source_property['scan']['inherited'] = False
    agg_col_source_property['classifications']['inherited'] = False
    agg_col_source_property['sources']['inherited'] = False
    agg_col_source_property['targets']['inherited'] = False
    agg_col_source_property['pipelines']['inherited'] = False
    agg_col_source_property['actions']['inherited'] = False
    agg_col_source_property['advanced']['inherited'] = False
    agg_col_source_property['exportInfo']['inherited'] = False


def get_temp_file_data(service_type, request):
    initial_scan_data = request.config.cache.get('initial_scan_data', default=None)
    return initial_scan_data[service_type]


def get_temp_file_name(service_type, request):
    return get_temp_file_data(service_type, request)['file_name']


def get_file_system_service(request):
    source_parameters = SourceParameters(exclude_enable_global=True, exclude_external_drives=True)
    file_path = get_temp_file_data(ServiceType.FILESYS, request)['file_path']
    include_data_object: ServiceIncludeData = ServiceIncludeData(path=file_path,
                                                                 signing=True,
                                                                 index=False)
    service = ServiceObject(name=ServiceType.FILESYS, type=ServiceType.FILESYS, mode=ModeType.SOURCE,
                            include=[include_data_object],
                            exclude=[],
                            parameters=source_parameters)
    return service

def get_aws_service(request):
    aws_access_key = os.environ['AWS_ACCESS_KEY_ID']
    aws_secret_key = os.environ['AWS_SECRET_ACCESS_KEY']
    aws_region = os.environ['AWS_REGION']
    file_path = get_temp_file_data(ServiceType.AWS, request)['aws_path']
    source_parameters = SourceParameters(access_key=aws_access_key, secret_key=aws_secret_key, region=aws_region)
    include_data_object: ServiceIncludeData = ServiceIncludeData(path=file_path,
                                                                 signing=True,
                                                                 index=False)
    service = ServiceObject(name=ServiceType.AWS, type=ServiceType.AWS, mode=ModeType.SOURCE,
                            include=[include_data_object],
                            exclude=[],
                            parameters=source_parameters)
    return service

def get_smb_service(request):
    smb_username = os.environ.get('SMB_USERNAME')
    smb_password = os.environ.get('SMB_PASSWORD')
    smb_domain = os.environ.get('SMB_DOMAIN')
    file_path = get_temp_file_data(ServiceType.SMB, request)['smb_path']
    smb_key = "smb://{0}".format(smb_domain)
    source_parameters = SourceParameters(password=smb_password, username=smb_username, server=smb_domain)
    include_data_object: ServiceIncludeData = ServiceIncludeData(path=file_path,
                                                                 signing=True,
                                                                 index=False)
    service = ServiceObject(name=ServiceType.SMB, type=ServiceType.SMB, mode=ModeType.SOURCE,
                            include=[include_data_object],
                            exclude=[],
                            parameters=source_parameters,
                            key= smb_key)
    return service

def get_s3_service(request):
    s3_endpoint = os.environ.get('MINIO_ENDPOINT')
    s3_access_key= os.environ.get('MINIO_ACCESS_KEY')
    s3_secret_key= os.environ.get('MINIO_SECRET_KEY')
    file_path = get_temp_file_data(ServiceType.OBJSTORE, request)['s3_path']
    source_parameters = SourceParameters(url=s3_endpoint, access_key=s3_access_key, secret_key=s3_secret_key)
    include_data_object: ServiceIncludeData = ServiceIncludeData(path=file_path,
                                                                 signing=True,
                                                                 index=False)
    service = ServiceObject(name=ServiceType.OBJSTORE, type=ServiceType.OBJSTORE, mode=ModeType.SOURCE,
                            include=[include_data_object],
                            exclude=[],
                            parameters=source_parameters)
    return service

class ScanHelper(BaseHelper):
    def __init__(self, private_client=None, public_client=None):
        super().__init__(private_client=private_client, public_client=public_client)

    def wait_scan_to_be_finished(self, aggregator_collector_object_id, is_scan_in_progress=False,
                                 is_initial_scan_started=False, wait_count=0):
        wait_time = START_WAITING_TIME if is_scan_in_progress else POLLING_TIME
        time.sleep(wait_time)

        if wait_count < WAITING_COUNT:
            properties_response = self.private_client.database_property_get(
                object_id=aggregator_collector_object_id,
                property_id=PropertyId.TASK_STATUS,
                options='{"infoLevel":"full"}')
            active_tree = properties_response['data']['activeTree']

            if bool(active_tree) or (not is_scan_in_progress and is_initial_scan_started):
                self.wait_scan_to_be_finished(aggregator_collector_object_id, True, True, wait_count + 1)
            elif not is_scan_in_progress and not is_initial_scan_started:
                self.wait_scan_to_be_finished(aggregator_collector_object_id, False, False, wait_count + 1)

    def execute_scan_now(self, aggregator_collector_object_id):
        return self.scan_now_with_multiple_attempts(aggregator_collector_object_id)

    def scan_now_with_multiple_attempts(self, aggregator_collector_object_id, max_retries=50):
        control_command_request = ControlCommandRequestBody(object_id=aggregator_collector_object_id,
                                                            command_id=CommandId.QUEUE_SCAN)
        scan_now_command_response = None
        for retry in range(1, max_retries + 1):
            scan_now_command_response = self.private_client.database_control_put(
                control_command_request=control_command_request)
            if scan_now_command_response['status'] == StatusEnum.OK:
                break
            time.sleep(POLLING_TIME)
        return scan_now_command_response

    def execute_core_scan(self, agg_col_id, request):
        file_system_service = get_file_system_service(request)
        file_system_valid_service = self.get_validated_source(agg_col_id, file_system_service)

        aws_service = get_aws_service(request)
        aws_valid_service = self.get_validated_source(agg_col_id, aws_service)

        smb_service = get_smb_service(request)
        smb_valid_service = self.get_validated_source(agg_col_id, smb_service)

        s3_service = get_s3_service(request)
        s3_valid_service = self.get_validated_source(agg_col_id, s3_service)

        validated_services = [file_system_valid_service, aws_valid_service, smb_valid_service, s3_valid_service]
        self.start_core_scan(agg_col_id, validated_services)
        self.wait_scan_to_be_finished(agg_col_id)

    def start_core_scan(self, agg_col_id, services):
        agg_col_properties = self.private_client.database_property_get(object_id=agg_col_id,
                                                                       property_id=PropertyId.POLICY,
                                                                       options='{"infoLevel":"full"}')

        agg_col_source_property = agg_col_properties.get('data')
        agg_col_source_property['sources']['values']['services'] = services
        set_inherited_as_false(agg_col_source_property)
        create_property_request: CreatePropertyRequestBody = CreatePropertyRequestBody(object_id=agg_col_id,
                                                                                       property_id=PropertyId.POLICY,
                                                                                       _property=agg_col_source_property)
        self.private_client.database_property_post(create_property_body=create_property_request)
        scan_now_command_response = self.execute_scan_now(agg_col_id)
        assert scan_now_command_response['status'] == StatusEnum.OK

    def validate_source_property(self, agg_col_id, service):
        validation_request_body: CreatePropertyRequestBody = CreatePropertyRequestBody(object_id=agg_col_id,
                                                                                       syntax_only=False,
                                                                                       service=service)
        validation_results = self.private_client.services_validate_put(
            validate_service_body=validation_request_body)
        return validation_results

    def get_validated_source(self, agg_col_id, service):
        validation_results = self.validate_source_property(agg_col_id, service)
        validation_results_data = validation_results.get('data')
        return validation_results_data.get('service')
