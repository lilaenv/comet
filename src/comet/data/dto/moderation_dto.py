from dataclasses import dataclass


@dataclass
class ModerationDTO:
    moderation_id: str
    category_scores: dict[str, float]
    flagged: bool
