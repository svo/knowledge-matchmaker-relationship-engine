import os

import anthropic

from knowledge_matchmaker_relationship_engine.domain.model.relationship import RelationshipType
from knowledge_matchmaker_relationship_engine.domain.service.relationship_classifier import RelationshipClassifier


class ClaudeRelationshipClassifier(RelationshipClassifier):
    def __init__(self) -> None:
        self._client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    def classify(self, thinking_summary: str, title: str, chunk_text: str) -> tuple[RelationshipType, str]:
        tools = [
            {
                "name": "classify_relationship",
                "description": "Classify the relationship between the user's thinking and a work.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "relationship_type": {
                            "type": "string",
                            "enum": ["RESONANCE", "CONFLICT", "BLIND_SPOT", "OPEN_SPACE"],
                        },
                        "reason": {
                            "type": "string",
                        },
                    },
                    "required": ["relationship_type", "reason"],
                },
            }
        ]

        messages = [
            {
                "role": "user",
                "content": (
                    f"User's thinking: {thinking_summary}\n\n"
                    f"Work title: {title}\n\n"
                    f"Excerpt: {chunk_text}\n\n"
                    "Classify the relationship between the user's thinking and this work. "
                    "Do NOT describe or summarize what the work says. "
                    "Return only the relationship type and a one-sentence reason why it matters to the user's specific thinking."
                ),
            }
        ]

        response = self._client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=256,
            tools=tools,
            tool_choice={"type": "tool", "name": "classify_relationship"},
            messages=messages,
        )

        tool_use = next(block for block in response.content if block.type == "tool_use")
        relationship_type = RelationshipType(tool_use.input["relationship_type"])
        reason = tool_use.input["reason"]

        return relationship_type, reason
