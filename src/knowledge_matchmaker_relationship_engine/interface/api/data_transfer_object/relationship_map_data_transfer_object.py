from typing import Any

from pydantic import BaseModel


class BuildRelationshipMapRequestDto(BaseModel):
    draft: str


class PointerDto(BaseModel):
    title: str
    source_url: str
    relationship_type: str
    reason: str

    @classmethod
    def from_domain_model(cls, domain_model: Any) -> "PointerDto":
        return cls(
            title=domain_model.title,
            source_url=domain_model.source_url,
            relationship_type=domain_model.relationship_type.value,
            reason=domain_model.reason,
        )


class RelationshipMapResponseDto(BaseModel):
    relationships: list[PointerDto]

    @classmethod
    def from_domain_model(cls, domain_model: Any) -> "RelationshipMapResponseDto":
        return cls(
            relationships=[PointerDto.from_domain_model(p) for p in domain_model.pointers],
        )
