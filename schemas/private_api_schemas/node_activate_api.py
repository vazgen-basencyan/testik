from pydantic import BaseModel

from schemas.base_schemas import StatusEnum


class NodeActivateResponse(BaseModel):
    status: StatusEnum
    data: dict
