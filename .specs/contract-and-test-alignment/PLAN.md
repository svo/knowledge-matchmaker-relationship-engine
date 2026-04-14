# Plan: Align Contracts, Complete Invariant Tests, and Persist ChromaDB

## Implementation Strategy

Four independent workstreams, ordered by dependency:

1. **Consumer contract update** (infrastructure adapter + application use case) — update `ThinkingExtractorHttpClient` and `BuildRelationshipMapUseCase` for the new thinking-extractor response format
2. **Producer contract update** (interface layer) — rename response DTO field `pointers` → `relationships`
3. **Invariant test completion** (tests only) — add missing forbidden-field assertions
4. **Persistent Chroma** (infrastructure) — switch `ChromaCorpusQuery` from `EphemeralClient` to `PersistentClient`

Workstreams 2, 3, and 4 are independent of each other and of workstream 1.

## Changes

### 1. Consumer contract update

**`infrastructure/http/thinking_extractor_http_client.py`**

Current:
```python
def extract(self, draft_text: str) -> list[dict]:
    response = client.post(f"{self._base_url}/extract", json={"text": draft_text})
    positions: list[dict] = response.json()["positions"]
    return positions
```

Target:
```python
def extract(self, draft_text: str) -> dict[str, list[str]]:
    response = client.post(f"{self._base_url}/extract", json={"draft": draft_text})
    data = response.json()
    return {"claims": data["claims"], "assumptions": data["assumptions"], "framings": data["framings"]}
```

- Change request payload: `{"text": draft_text}` → `{"draft": draft_text}`
- Change response parsing: read `claims`, `assumptions`, `framings` instead of `positions`
- Update return type from `list[dict]` to `dict[str, list[str]]`

**`domain/service/thinking_extractor_client.py`** (port)

- Update abstract method signature: `extract(draft_text: str) -> dict[str, list[str]]`

**`application/use_case/build_relationship_map_use_case.py`**

Current:
```python
positions = self._thinking_extractor_client.extract(draft_text)
thinking_summary = " ".join(p["text"] for p in positions)
```

Target:
```python
extracted = self._thinking_extractor_client.extract(draft_text)
all_positions = extracted["claims"] + extracted["assumptions"] + extracted["framings"]
thinking_summary = " ".join(all_positions)
```

### 2. Producer contract update

**`interface/api/data_transfer_object/relationship_map_data_transfer_object.py`**

- Rename `RelationshipMapResponseDto.pointers` → `RelationshipMapResponseDto.relationships`
- Update `from_domain_model()`: `pointers=[...]` → `relationships=[...]`

**`interface/api/controller/relationship_map_controller.py`**

- No change needed — the controller calls `from_domain_model()` which handles the mapping

### 3. Invariant test completion

**`tests/.../domain/model/test_relationship.py`**

Add three new tests:
```python
def test_pointer_should_not_have_abstract_field():
    assert_that(Pointer.model_fields).does_not_contain_key("abstract")

def test_pointer_should_not_have_text_field():
    assert_that(Pointer.model_fields).does_not_contain_key("text")

def test_pointer_should_not_have_body_field():
    assert_that(Pointer.model_fields).does_not_contain_key("body")
```

**`tests/.../interface/api/controller/test_relationship_map_controller.py`**

Add DTO-level invariant tests for the same five forbidden fields on `PointerDto`.

### 4. Persistent Chroma

**`infrastructure/chroma/chroma_corpus_query.py`**

Current:
```python
self._chroma_client = chromadb.EphemeralClient()
```

Target:
```python
chroma_data_path = os.environ.get("CHROMA_DATA_PATH", "/data/chroma")
self._chroma_client = chromadb.PersistentClient(path=chroma_data_path)
```

## Task List

### Consumer contract update

1. [ ] Update `ThinkingExtractorClient` port: change return type to `dict[str, list[str]]`
2. [ ] Update `ThinkingExtractorHttpClient`: send `{"draft": ...}`, parse `claims`/`assumptions`/`framings`
3. [ ] Update `BuildRelationshipMapUseCase`: aggregate thinking summary from the new structure
4. [ ] Update use case tests: mock extractor returns new format, verify summary aggregation
5. [ ] Update HTTP client tests: mock responses use new thinking-extractor contract
6. [ ] Run `tox` to verify

### Producer contract update

7. [ ] Rename `RelationshipMapResponseDto.pointers` → `RelationshipMapResponseDto.relationships`
8. [ ] Update `from_domain_model()` in the DTO
9. [ ] Update controller integration tests: assert response contains `relationships` key, not `pointers`
10. [ ] Run `tox` to verify

### Invariant test completion

11. [ ] Add `test_pointer_should_not_have_abstract_field` to domain model tests
12. [ ] Add `test_pointer_should_not_have_text_field` to domain model tests
13. [ ] Add `test_pointer_should_not_have_body_field` to domain model tests
14. [ ] Add DTO-level invariant tests for all five forbidden fields on `PointerDto`
15. [ ] Run `tox` to verify

### Persistent Chroma

16. [ ] Modify `ChromaCorpusQuery.__init__` to use `PersistentClient` with configurable path via `CHROMA_DATA_PATH`
17. [ ] Update tests to use `tmp_path` for isolated persistent Chroma
18. [ ] Run `tox` to verify

## Testing Strategy

**Unit tests**: Use case tests with mocked extractor returning the new format. Domain model invariant tests for all five forbidden fields. HTTP client tests with mocked httpx responses matching new contract.

**Integration tests**: Controller tests verify response key is `relationships`. Negative test verifying `pointers` key is absent.

**Invariant tests**: 5 tests on `Pointer` model fields + 5 tests on `PointerDto` fields = 10 invariant assertions total.

## Risks and Mitigations

- **Risk**: `ThinkingExtractorClient` return type change breaks all mocks in tests. **Mitigation**: Update all test fixtures in the same commit; `tox` (mypy) will catch any missed references.
- **Risk**: Chroma `PersistentClient` requires the mount path to exist at startup. **Mitigation**: Add `os.makedirs(path, exist_ok=True)` before creating the client, or document that the Vagrantfile creates the volume.
