from typing import List

from pydantic import BaseModel
from schemas.base_schemas import NodeId, ModeType
from schemas.private_api_schemas.parameters_api import SourceParameters


class ServiceIncludeData(BaseModel):
    signing: bool
    index: bool
    path: str


class ServicesInfoEstimations(BaseModel):
    accessCost: int
    accessDelay: int
    accessRate: int
    storeCost: int


class IncludeObjectInfo(BaseModel):
    index: bool
    signing: bool
    path: str


class ServicesInfo(BaseModel):
    actions: object
    estimation: ServicesInfoEstimations
    include: List[IncludeObjectInfo]
    key: str
    name: str
    type: NodeId
    mode: ModeType
    parameters: SourceParameters


class CostEstimation(BaseModel):
    accessCost: int
    accessDelay: int
    accessRate: int
    storeCost: int


class ServiceObject(BaseModel):
    name: str
    type: NodeId
    mode: ModeType
    include: List[ServiceIncludeData]
    exclude: List[str]
    parameters: SourceParameters
    cost_estimation: CostEstimation

