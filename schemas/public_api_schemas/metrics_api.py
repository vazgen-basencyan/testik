from pydantic import BaseModel

from schemas.base_schemas import StatusEnum, ApiError


class MetricsApiPositiveResponse(BaseModel):
    data: str


class MetricsApiNegativeResponse(BaseModel):
    status: StatusEnum
    name: str
    message: str
    error: ApiError
