from dataclasses import dataclass, field
from datetime import datetime
import uuid


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@dataclass
class Note:
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    title: str = "Untitled Note"
    content: str = ""
    created_at: str = field(default_factory=_now)
    updated_at: str = field(default_factory=_now)

    def touch(self) -> None:
        self.updated_at = _now()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @staticmethod
    def from_dict(data: dict) -> "Note":
        return Note(
            id=data.get("id", uuid.uuid4().hex),
            title=data.get("title", "Untitled Note"),
            content=data.get("content", ""),
            created_at=data.get("created_at", _now()),
            updated_at=data.get("updated_at", _now()),
        )

    def preview(self, length: int = 70) -> str:
        text = " ".join(self.content.split())
        if len(text) <= length:
            return text
        return text[:length].rstrip() + "..."

    def matches(self, query: str) -> bool:
        query = query.strip().lower()
        if not query:
            return True
        return query in self.title.lower() or query in self.content.lower()
