from pytest_archon.rule import archrule


def test_should_maintain_domain_layer_independence():
    (
        archrule(
            "Domain Layer Independence",
            comment="Domain layer should not depend on other layers (Clean Architecture)",
        )
        .match("knowledge_matchmaker_relationship_engine.domain.*")
        .should_not_import(
            "knowledge_matchmaker_relationship_engine.infrastructure.*",
            "knowledge_matchmaker_relationship_engine.interface.*",
            "knowledge_matchmaker_relationship_engine.application.*",
        )
        .check("knowledge_matchmaker_relationship_engine")
    )


def test_should_maintain_application_interface_independence():
    (
        archrule(
            "Application Interface",
            comment="Application layer should not depend on interface layer",
        )
        .match("knowledge_matchmaker_relationship_engine.application.*")
        .should_not_import("knowledge_matchmaker_relationship_engine.interface.*")
        .check("knowledge_matchmaker_relationship_engine")
    )


def test_should_maintain_application_infrastructure_independence():
    (
        archrule(
            "Application Infrastructure",
            comment="Application layer should not depend on infrastructure layer",
        )
        .match("knowledge_matchmaker_relationship_engine.application.*")
        .should_not_import("knowledge_matchmaker_relationship_engine.infrastructure.*")
        .check("knowledge_matchmaker_relationship_engine")
    )


def test_should_use_application_use_case_in_controller():
    (
        archrule(
            "Controller Use Case",
            comment="Interface controller should depend on application use cases",
        )
        .match("knowledge_matchmaker_relationship_engine.interface.api.controller.*")
        .should_import("knowledge_matchmaker_relationship_engine.application.use_case.*")
        .check("knowledge_matchmaker_relationship_engine")
    )


def test_should_not_use_domain_model_in_data_transfer_object():
    (
        archrule(
            "Data Transfer Object Model",
            comment="Data Transfer Object should not depend directly on domain model",
        )
        .match("knowledge_matchmaker_relationship_engine.interface.api.data_transfer_object.*")
        .should_not_import("knowledge_matchmaker_relationship_engine.domain.model.*")
        .check("knowledge_matchmaker_relationship_engine")
    )


def test_should_follow_security_module_architecture():
    (
        archrule(
            "Security Module",
            comment="Security components should follow architectural boundaries",
        )
        .match("knowledge_matchmaker_relationship_engine.infrastructure.security.*")
        .should_import("knowledge_matchmaker_relationship_engine.domain.authentication.*")
        .check("knowledge_matchmaker_relationship_engine")
    )


def test_should_not_have_circular_dependencies():
    (
        archrule(
            "No Circular Dependencies",
            comment="No modules should have circular dependencies",
        )
        .match("knowledge_matchmaker_relationship_engine.*")
        .should(
            lambda module, direct_imports, all_imports: module not in direct_imports
            and module not in all_imports.get(module, set()),
            "no_circular_dependencies",
        )
        .check("knowledge_matchmaker_relationship_engine")
    )


def test_should_maintain_shared_module_independence():
    (
        archrule(
            "Shared Module Dependencies",
            comment="Shared module should not depend on application, infrastructure or interface",
        )
        .match("knowledge_matchmaker_relationship_engine.shared.*")
        .should_not_import(
            "knowledge_matchmaker_relationship_engine.application.*",
            "knowledge_matchmaker_relationship_engine.infrastructure.*",
            "knowledge_matchmaker_relationship_engine.interface.*",
        )
        .check("knowledge_matchmaker_relationship_engine")
    )


def test_should_have_no_fastapi_imports_in_domain():
    (
        archrule(
            "Domain FastAPI Independence",
            comment="Domain layer should not import FastAPI",
        )
        .match("knowledge_matchmaker_relationship_engine.domain.*")
        .should_not_import("fastapi.*")
        .check("knowledge_matchmaker_relationship_engine")
    )
