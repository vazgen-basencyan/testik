from typing import List

from pydantic import BaseModel

from schemas.base_schemas import StatusEnum, ApiError


class UserData(BaseModel):
    provider: str
    userId: str
    objectId: str
    name: str
    homeId: str
    organization: str
    email: str
    phone: str
    language: str
    token: str
    isActivated: bool
    isRoot: bool
    permissions: List[str]


class LoginResponse(BaseModel):
    status: StatusEnum
    data: UserData


class LoginError(BaseModel):
    status: StatusEnum
    name: str
    message: str
    error: dict


class LoginNegativeResponse(BaseModel):
    status: StatusEnum
    name: str
    message: str
    error: ApiError

