from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ArticleContent:
    text_data: str
    table_data: List[dict] = None

    def to_dict(self):
        return {
            "text_data": self.text_data,
            "table_data": self.table_data
        }
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            text_data=data.get("text_content", ""),
            table_data=data.get("table_data", [])
        )

@dataclass
class StandardArticle:
    url: str
    content: Optional[ArticleContent]
    title: Optional[str] = None

    def to_dict(self):
        return {
            "url": self.url,
            "content": self.content.to_dict() if self.content else None,
            "title": self.title
        }
