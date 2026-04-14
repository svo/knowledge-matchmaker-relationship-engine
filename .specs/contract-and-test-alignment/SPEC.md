# Feature: Align Contracts, Complete Invariant Tests, and Persist ChromaDB

## Overview

The relationship-engine has four categories of gap:

1. **Consumer contract update** — the thinking-extractor is changing its `POST /extract` contract (request field `text` → `draft`, response from flat `positions` to separate `claims`/`assumptions`/`framings` arrays). The `ThinkingExtractorHttpClient` must be updated to match.
2. **Producer contract deviation** — the `POST /map` response uses `pointers` as the collection key, but the canonical spec defines it as `relationships`.
3. **Incomplete invariant tests** — the plan requires asserting that the `Pointer` schema contains no field named `content`, `summary`, `abstract`, `text`, or `body`. Currently only `summary` and `content` are tested.
4. **Ephemeral storage** — `ChromaCorpusQuery` uses `chromadb.EphemeralClient()`, creating its own empty in-memory store instead of reading from the shared persistent store populated by the corpus-indexer.

## Motivation

### Consumer contract

The relationship-engine is the sole consumer of the thinking-extractor. Its HTTP client currently sends `{"text": draft_text}` and reads `response.json()["positions"]`. After the thinking-extractor contract changes, this will break. The client must be updated to send `{"draft": draft_text}` and parse the `claims`, `assumptions`, and `framings` arrays.

The use case currently aggregates positions into a thinking summary via `" ".join(p["text"] for p in positions)`. With the new contract, it should aggregate across all three arrays.

### Producer contract

The canonical spec defines the response key as `relationships`:
```json
{ "relationships": [{ "title", "source_url", "relationship_type", "reason" }] }
```

The implementation uses `pointers`. While `Pointer` is the correct domain model name (it's a pointer to literature, not the relationship itself), the API-level key should match the spec. The DTO maps between domain and wire representation — this is exactly the kind of translation DTOs exist for.

### Invariant tests

The plan's testing strategy explicitly requires: "Assert that `Pointer` response schema contains no field named `content`, `summary`, `abstract`, `text`, or `body`." This is the critical design constraint (matchmaker, not messenger) expressed as a test. Only 2 of 5 forbidden fields are currently tested.

### Persistent Chroma

The `ChromaCorpusQuery` creates `chromadb.EphemeralClient()` — a fresh, empty Chroma instance in memory. This means the relationship-engine can never find any documents indexed by the corpus-indexer. It must use `chromadb.PersistentClient()` pointed at the same shared volume the corpus-indexer writes to.

## Acceptance Criteria

### Consumer contract

- [ ] Given the thinking-extractor returns `{ "claims": [...], "assumptions": [...], "framings": [...] }`, when the relationship-engine calls it, then `ThinkingExtractorHttpClient` correctly parses all three arrays.
- [ ] Given the thinking-extractor expects `{ "draft": "..." }`, when the relationship-engine calls it, then the HTTP client sends `draft` (not `text`).
- [ ] Given positions from all three categories, when the use case builds a thinking summary, then claims, assumptions, and framings are all included.

### Producer contract

- [ ] Given a successful `POST /map` call, when the response is returned, then the JSON contains `relationships` as the top-level key.
- [ ] Given a successful `POST /map` call, when the response is returned, then no field named `pointers` exists at the top level.

### Invariant tests

- [ ] Given the `Pointer` domain model, when its fields are inspected, then it does not contain `content`, `summary`, `abstract`, `text`, or `body` — one test per forbidden field (5 tests total).
- [ ] Given the `PointerDto` response schema, when its fields are inspected, then it does not contain `content`, `summary`, `abstract`, `text`, or `body`.

### Persistence

- [ ] Given a corpus indexed by the corpus-indexer, when the relationship-engine queries Chroma, then it finds the indexed documents.
- [ ] Given the Chroma data path is configurable via `CHROMA_DATA_PATH`, when set, then `PersistentClient` uses that path.

## Current State

### ThinkingExtractorHttpClient (`infrastructure/http/thinking_extractor_http_client.py`)

```python
def extract(self, draft_text: str) -> list[dict]:
    with httpx.Client() as client:
        response = client.post(
            f"{self._base_url}/extract",
            json={"text": draft_text},  # Should be: "draft"
        )
        response.raise_for_status()
        positions: list[dict] = response.json()["positions"]  # Should parse claims/assumptions/framings
        return positions
```

### Response DTO (`relationship_map_data_transfer_object.py`)

```python
class RelationshipMapResponseDto(BaseModel):
    pointers: list[PointerDto]  # Should be: relationships
```

### Invariant tests (`test_relationship.py`)

```python
def test_pointer_should_not_have_summary_field():
    assert_that(Pointer.model_fields).does_not_contain_key("summary")

def test_pointer_should_not_have_content_field():
    assert_that(Pointer.model_fields).does_not_contain_key("content")

# Missing: abstract, text, body
```

### Ephemeral Chroma (`chroma_corpus_query.py`)

```python
self._chroma_client = chromadb.EphemeralClient()  # Should be: PersistentClient
```

## Target Contract

### Consumer (thinking-extractor `POST /extract`)

```json
Request:  { "draft": "string" }
Response: { "claims": ["string"], "assumptions": ["string"], "framings": ["string"] }
```

### Producer (`POST /map`)

```json
Request:  { "draft": "string" }
Response: {
  "relationships": [
    { "title": "string", "source_url": "string", "relationship_type": "RESONANCE|CONFLICT|BLIND_SPOT|OPEN_SPACE", "reason": "string" }
  ]
}
```

## Domain Model Impact

- `RelationshipMap.pointers` stays as-is in the domain (it's the correct domain term)
- `RelationshipMapResponseDto.pointers` → `RelationshipMapResponseDto.relationships` (DTO field name only)
- `ThinkingExtractorClient.extract()` return type: currently `list[dict]`, should become a structured type or the method should return separate lists
- `BuildRelationshipMapUseCase.execute()`: update thinking summary aggregation to use the new response structure

## Cross-Service Dependencies

- **Depends on**: thinking-extractor contract change (must land first or simultaneously)
- **Depended on by**: UI must update `RelationshipMap.pointers` → `RelationshipMap.relationships`
- **Depends on**: parent repo Vagrantfile shared Chroma volume (for persistent storage)

## Open Questions

None.
