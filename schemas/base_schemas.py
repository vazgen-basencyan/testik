from enum import Enum
from typing import Optional

from pydantic import BaseModel


class StatusEnum(str, Enum):
    OK = 'OK'
    ERROR = 'ERROR'
    ok = 'ok'
    error = 'error'


class CommandParams(BaseModel):
    commandId: str


class ApiError(BaseModel):
    name: str
    message: str
    params: Optional[CommandParams] = None


class StringResponse(BaseModel):
    data: str


class NodeId(str, Enum):
    APPAGT = 'appagt'
    GROUP = 'group'
    USER = 'user'


class ModeType(str, Enum):
    SOURCE = 'Source'
    TARGET = 'Target'


class ServiceType(str, Enum):
    FILESYS = 'filesys'
    AWS = 'aws'
    OBJSTORE = 'objstore'
    SMB = 'smb'
    MS_ONEDRIVE = 'ms-onedrive'
    AZURE = 'azure'


class SetupConfigs(BaseModel):
    autotest_username: str
    autotest_password: str
    autotest_email: str
    root_username: str
    root_password: str
    host: str
    base_path: str
    hybrid_port: str
    version: str
    scan_folder: str


class PropertyId(str, Enum):
    PID_POLICY = 'PID_POLICY'
    PID_TASK_STATUS = 'PID_TASK_STATUS'
    PID_MEMBERS = 'PID_MEMBERS'
    PID_TRUSTEES = 'PID_TRUSTEES'

class CommonStatusResponse(BaseModel):
    status: StatusEnum
    data: dict
