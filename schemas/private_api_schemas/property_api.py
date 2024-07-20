from typing import List

from pydantic import BaseModel
from typing import Optional

from schemas.base_schemas import StatusEnum
from schemas.private_api_schemas.object_api import ObjectInfo
from schemas.private_api_schemas.settings_api import RootSettings
from schemas.private_api_schemas.services_api import ServicesInfo


class PropertyOptions(BaseModel):
    physicalOnly: bool
    infoLevel: str
    effective: bool
    lineNumber: float
    consoleCommand: str
    messages: bool
    security: bool
    getObjects: bool
    getHistoricTree: bool
    getActiveTree: bool
    getWorkers: bool
    nodeIdFilter: List[str]
    age: float
    getPending: bool
    getPostponed: bool
    getSolved: bool
    getPolicies: bool
    getAllPolicies: bool
    getRules: bool
    getPolicyId: str


class PropertySourcesValues(BaseModel):
    services: List[str]
    items: ServicesInfo


class PropertySources(BaseModel):
    values: PropertySourcesValues


class PropertyData(BaseModel):
    object: ObjectInfo
    permissions: List[str]
    items: Optional[str] = None
    rootSettings: Optional[RootSettings] = None
    sources: Optional[PropertySources] = None
    objects: Optional[dict] = None
    historicTree: Optional[dict] = None
    activeTree: Optional[dict] = None


class PropertyResponse(BaseModel):
    status: StatusEnum
    data: List[PropertyData] = []

