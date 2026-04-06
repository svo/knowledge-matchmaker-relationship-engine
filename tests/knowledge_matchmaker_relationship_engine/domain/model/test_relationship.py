from assertpy import assert_that

from knowledge_matchmaker_relationship_engine.domain.model.relationship import Pointer, RelationshipType


def test_should_have_title():
    pointer = Pointer(title="Being and Time", source_url="https://example.com", relationship_type=RelationshipType.CONFLICT, reason="Challenges your view.")
    assert_that(pointer.title).is_equal_to("Being and Time")


def test_should_have_source_url():
    pointer = Pointer(title="Being and Time", source_url="https://example.com", relationship_type=RelationshipType.CONFLICT, reason="Challenges your view.")
    assert_that(pointer.source_url).is_equal_to("https://example.com")


def test_should_have_relationship_type():
    pointer = Pointer(title="Being and Time", source_url="https://example.com", relationship_type=RelationshipType.CONFLICT, reason="Challenges your view.")
    assert_that(pointer.relationship_type).is_equal_to(RelationshipType.CONFLICT)


def test_should_have_reason():
    pointer = Pointer(title="Being and Time", source_url="https://example.com", relationship_type=RelationshipType.CONFLICT, reason="Challenges your view.")
    assert_that(pointer.reason).is_equal_to("Challenges your view.")


def test_pointer_should_not_have_summary_field():
    assert_that(Pointer.model_fields).does_not_contain_key("summary")


def test_pointer_should_not_have_content_field():
    assert_that(Pointer.model_fields).does_not_contain_key("content")
