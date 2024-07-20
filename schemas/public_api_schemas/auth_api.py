from typing import List
from pydantic import BaseModel

from schemas.base_schemas import StatusEnum, ApiError


class State(BaseModel):
    provider: str
    id: str
    clientObjectId: str
    timestamp: int


class AuthenticationProvider(BaseModel):
    provider: str
    name: str
    icon: str
    uri: str
    state: State


class AuthApiResponse(BaseModel):
    status: StatusEnum
    data: List[AuthenticationProvider]


class AuthApiNegativeResponse(BaseModel):
    status: StatusEnum
    name: str
    message: str
    error: ApiError
