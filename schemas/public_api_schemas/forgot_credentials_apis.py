from pydantic import BaseModel

from schemas.base_schemas import StatusEnum


class ForgotCredentialsApiResponse(BaseModel):
    status: StatusEnum
    data: dict
