from pydantic import BaseModel

from schemas.base_schemas import StatusEnum


class ChangeLogApiResponse(BaseModel):
    status: StatusEnum
    data: str
