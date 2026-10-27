
import unicodedata

from pydantic import BaseModel, Field, field_validator


class CustomerMessage(BaseModel):
    text: str = Field(
        min_length=1,
        max_length=5000,
        description="Untrusted customer-provided text.",
    )

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        normalized = value.strip()

        if not normalized:
            raise ValueError("Message must not be blank.")

        if not any(character.isprintable() for character in normalized):
            raise ValueError("Message must contain printable text.")

        # Reject unexpected control characters while permitting
        # ordinary whitespace such as tabs and newlines.
        for character in normalized:
            if unicodedata.category(character) == "Cc":
                if character not in "\t\n\r":
                    raise ValueError(
                        "Message contains unsupported control characters."
                    )

        return normalized
