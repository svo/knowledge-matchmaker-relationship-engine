from unittest.mock import Mock

import pytest
from assertpy import assert_that
from fastapi import FastAPI
from fastapi.testclient import TestClient

from knowledge_matchmaker_relationship_engine.application.use_case.build_relationship_map_use_case import (
    BuildRelationshipMapUseCase,
)
from knowledge_matchmaker_relationship_engine.domain.model.relationship import (
    Pointer,
    RelationshipMap,
    RelationshipType,
)
from knowledge_matchmaker_relationship_engine.interface.api.controller.relationship_map_controller import (
    RelationshipMapController,
)
from knowledge_matchmaker_relationship_engine.interface.api.data_transfer_object.relationship_map_data_transfer_object import (
    PointerDto,
)


class TestRelationshipMapController:
    @pytest.fixture
    def mock_use_case(self) -> Mock:
        mock = Mock(spec=BuildRelationshipMapUseCase)
        mock.execute.return_value = RelationshipMap(
            pointers=[
                Pointer(
                    title="Being and Time",
                    source_url="https://example.com/being",
                    relationship_type=RelationshipType.CONFLICT,
                    reason="Challenges your claim about distributed cognition.",
                )
            ]
        )
        return mock

    @pytest.fixture
    def controller(self, mock_use_case) -> RelationshipMapController:
        return RelationshipMapController(build_relationship_map_use_case=mock_use_case)

    @pytest.fixture
    def app(self, controller) -> FastAPI:
        app = FastAPI()
        app.include_router(controller.router)
        return app

    @pytest.fixture
    def client(self, app) -> TestClient:
        return TestClient(app)

    def test_should_return_200_when_map_is_called(self, client):
        response = client.post("/map", json={"draft": "My draft about cognition."})

        assert_that(response.status_code).is_equal_to(200)

    def test_should_return_pointers_in_response(self, client):
        response = client.post("/map", json={"draft": "My draft about cognition."})

        assert_that(response.json()["pointers"]).is_length(1)

    def test_should_not_return_summary_field_in_pointer(self):
        assert_that(PointerDto.model_fields).does_not_contain_key("summary")
