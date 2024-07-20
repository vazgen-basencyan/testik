from pydantic import BaseModel

from schemas.base_schemas import StatusEnum


class StateModel(BaseModel):
    isRunning: bool
    isConnected: bool
    isRegistered: bool
    isActivated: bool
    activationCode: str


class NodeModel(BaseModel):
    nodeId: str
    nodeName: str
    parentNodeId: str
    parentNodeName: str
    parentObjectId: str
    hostId: str
    hostName: str
    activationCode: str
    isActivated: bool
    bindTo: str


class PackageModel(BaseModel):
    moduleType: str
    dirName: str
    version: str
    engineVersion: str
    mfgLong: str
    mfgShort: str
    description: str
    isPlatform: bool
    isAppliance: bool
    isAgent: bool
    isAppAgt: bool
    isWorker: bool
    airGapped: bool
    productName: str


class CombinedModelData(BaseModel):
    pkg: PackageModel
    node: NodeModel
    state: StateModel


class ConfigApiResponse(BaseModel):
    status: StatusEnum
    data: CombinedModelData
