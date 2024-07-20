from typing import List

from pydantic import BaseModel


class SecureParameters(BaseModel):
    readonly: List[str]
    secure: List[str]
    token: str


class SourceParameters(BaseModel):
    excludeEnableGlobal: bool
    excludeExternalDrives: bool
    format: str
    server: str
    name: str
    username: str
    password: str
    tenant: str
    clientId: str
    clientSecret: str
    region: str
    auth: str
    secureParameters: SecureParameters
    token: str
