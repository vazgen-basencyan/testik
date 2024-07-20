from typing import List

from pydantic import BaseModel


class RootSettingsValues(BaseModel):
    enableUpdates: bool
    updateSlot: str
    updatePath: str
    updatePublicKeyPath: str


class InheritedFrom(BaseModel):
    objectId: str
    parentId: str
    classId: str
    name: str
    uniqueName: str
    flags: int
    tags: object
    createdAt: int
    updatedAt: int
    permissions: List[str]
    items: str
    isContainer: bool
    isOnline: bool
    isActivated: bool
    isReadyToWork: bool


class RootSettings(BaseModel):
    values: RootSettingsValues
    inherited: bool
    inheritedValues: RootSettingsValues
    inheritedFrom: InheritedFrom

