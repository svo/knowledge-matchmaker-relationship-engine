from enum import Enum
from pydantic import BaseModel


class RelationshipType(str, Enum):
    RESONANCE = "RESONANCE"
    CONFLICT = "CONFLICT"
    BLIND_SPOT = "BLIND_SPOT"
    OPEN_SPACE = "OPEN_SPACE"


class Pointer(BaseModel):
    title: str
    source_url: str
    relationship_type: RelationshipType
    reason: str


class RelationshipMap(BaseModel):
    pointers: list[Pointer]
