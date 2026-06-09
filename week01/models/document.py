from datetime import datetime, timezone
from typing import Annotated, Literal
from uuid import uuid4
from pydantic import BaseModel, Field, field_validator

# str que no acepta vacios ni solo espacios
NonEmptyStr = Annotated[str, Field(min_length=1)]

# valores validos para source
SourceType = Literal["pdf", "web", "csv", "manual"]

class DocumentRecord(BaseModel):
    model_config = {"frozen": False, "str_strip_whitespace": True}

    id: str = Field(default_factory=lambda: str(uuid4()))
    title: NonEmptyStr
    content: Annotated[str, Field(min_length=10)]
    source: SourceType
    language: str = "es"
    tags: list[str] = Field(default_factory=list)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(tz=timezone.utc)
    )

    @field_validator("tags")
    @classmethod
    def remove_duplicate_tags(cls, tags: list[str]) -> list[str]:
        return list(dict.fromkeys(tags))

    @field_validator("content")
    @classmethod
    def content_not_empty(cls, v:str) -> str:
        if not v:
            raise ValueError("content no puede estar vacío o contener solo espacios")
        return v
