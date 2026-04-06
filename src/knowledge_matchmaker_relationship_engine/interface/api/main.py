import sys
import uvicorn
from fastapi import FastAPI
from lagom import Container

from knowledge_matchmaker_relationship_engine.application.use_case.build_relationship_map_use_case import BuildRelationshipMapUseCase
from knowledge_matchmaker_relationship_engine.application.use_case.coconut_use_case import CreateCoconutUseCase, GetCoconutUseCase
from knowledge_matchmaker_relationship_engine.application.use_case.health_use_case import HealthUseCase
from knowledge_matchmaker_relationship_engine.domain.health.health_checker import HealthChecker
from knowledge_matchmaker_relationship_engine.domain.repository.coconut_repository import CoconutCommandRepository, CoconutQueryRepository
from knowledge_matchmaker_relationship_engine.domain.service.corpus_query import CorpusQuery
from knowledge_matchmaker_relationship_engine.domain.service.relationship_classifier import RelationshipClassifier
from knowledge_matchmaker_relationship_engine.domain.service.thinking_extractor_client import ThinkingExtractorClient
from knowledge_matchmaker_relationship_engine.infrastructure.chroma.chroma_corpus_query import ChromaCorpusQuery
from knowledge_matchmaker_relationship_engine.infrastructure.claude.claude_relationship_classifier import ClaudeRelationshipClassifier
from knowledge_matchmaker_relationship_engine.infrastructure.http.thinking_extractor_http_client import ThinkingExtractorHttpClient
from knowledge_matchmaker_relationship_engine.infrastructure.persistence.in_memory.in_memory_coconut_command_repository import (
    InMemoryCoconutCommandRepository,
)
from knowledge_matchmaker_relationship_engine.infrastructure.persistence.in_memory.in_memory_coconut_query_repository import (
    InMemoryCoconutQueryRepository,
)
from knowledge_matchmaker_relationship_engine.infrastructure.security.basic_authentication import (
    BasicAuthenticator,
    SecurityDependency,
    get_basic_authenticator,
)
from knowledge_matchmaker_relationship_engine.infrastructure.system.health_factory import create_health_checker
from knowledge_matchmaker_relationship_engine.interface.api.controller.coconut_controller import (
    create_coconut_controller,
)
from knowledge_matchmaker_relationship_engine.interface.api.controller.health_controller import create_health_controller
from knowledge_matchmaker_relationship_engine.interface.api.controller.relationship_map_controller import create_relationship_map_controller
from knowledge_matchmaker_relationship_engine.shared.configuration import get_application_setting_provider

app = FastAPI(title="Knowledge Matchmaker Relationship Engine API", version="1.0.0")


def get_container() -> Container:
    container = Container()

    query_repo = InMemoryCoconutQueryRepository()
    command_repo = InMemoryCoconutCommandRepository(query_repo)

    container[CoconutQueryRepository] = lambda: query_repo  # type: ignore
    container[CoconutCommandRepository] = lambda: command_repo  # type: ignore

    container[GetCoconutUseCase] = GetCoconutUseCase
    container[CreateCoconutUseCase] = CreateCoconutUseCase

    authenticator = get_basic_authenticator()
    security_dependency = SecurityDependency(authenticator)
    container[BasicAuthenticator] = lambda: authenticator
    container[SecurityDependency] = lambda: security_dependency

    health_checker = create_health_checker()

    container[HealthChecker] = lambda: health_checker  # type: ignore
    container[HealthUseCase] = HealthUseCase

    thinking_extractor_client = ThinkingExtractorHttpClient()
    corpus_query = ChromaCorpusQuery()
    relationship_classifier = ClaudeRelationshipClassifier()

    container[ThinkingExtractorClient] = lambda: thinking_extractor_client  # type: ignore
    container[CorpusQuery] = lambda: corpus_query  # type: ignore
    container[RelationshipClassifier] = lambda: relationship_classifier  # type: ignore
    container[BuildRelationshipMapUseCase] = BuildRelationshipMapUseCase

    return container


global_container = get_container()


def get_global_container() -> Container:
    return global_container


security_dependency = global_container[SecurityDependency]
authentication_dependency = security_dependency.authentication_dependency()

coconut_controller = create_coconut_controller(global_container, authentication_dependency)
app.include_router(coconut_controller.router)

health_use_case = global_container[HealthUseCase]
health_controller = create_health_controller(health_use_case)
app.include_router(health_controller)

build_relationship_map_use_case = global_container[BuildRelationshipMapUseCase]
relationship_map_controller = create_relationship_map_controller(build_relationship_map_use_case)
app.include_router(relationship_map_controller.router)


def main(args: list) -> None:
    settings_provider = get_application_setting_provider()
    reload_setting = settings_provider.get("reload")
    host_setting = settings_provider.get("host")

    uvicorn.run(
        "knowledge_matchmaker_relationship_engine.interface.api.main:app",
        reload=reload_setting,
        host=host_setting,
    )


def run() -> None:
    main(sys.argv[1:])
