from fastapi import APIRouter

from knowledge_matchmaker_relationship_engine.application.use_case.build_relationship_map_use_case import (
    BuildRelationshipMapUseCase,
)
from knowledge_matchmaker_relationship_engine.interface.api.data_transfer_object.relationship_map_data_transfer_object import (
    BuildRelationshipMapRequestDto,
    RelationshipMapResponseDto,
)


class RelationshipMapController:
    def __init__(self, build_relationship_map_use_case: BuildRelationshipMapUseCase) -> None:
        self._build_relationship_map_use_case = build_relationship_map_use_case
        self.router = APIRouter(prefix="/map", tags=["map"])
        self._register_routes()

    def _register_routes(self) -> None:
        self.router.add_api_route(
            "",
            self.build_map,
            methods=["POST"],
            response_model=RelationshipMapResponseDto,
        )

    async def build_map(self, request: BuildRelationshipMapRequestDto) -> RelationshipMapResponseDto:
        relationship_map = self._build_relationship_map_use_case.execute(request.draft)
        return RelationshipMapResponseDto.from_domain_model(relationship_map)


def create_relationship_map_controller(
    build_relationship_map_use_case: BuildRelationshipMapUseCase,
) -> RelationshipMapController:
    return RelationshipMapController(build_relationship_map_use_case=build_relationship_map_use_case)
