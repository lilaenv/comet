from pydantic import BaseModel


class ModerationDTO(BaseModel):
    moderation_id: str
    category_scores: dict[str, float]
    flagged: bool
