from typing import Optional

from pydantic import BaseModel


class ObjectInfo(BaseModel):
    objectId: str
    parentId: str
    classId: str
    name: str
    uniqueName: str
    flags: int
    tags: dict
    isContainer: Optional[bool] = None
    isActivated: Optional[bool] = None
    isOnline: Optional[bool] = None
    isReadyToWork: Optional[bool] = None
