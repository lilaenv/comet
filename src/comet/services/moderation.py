import json

from openai import OpenAI
from openai._compat import model_json

from src.comet.cli import parse_args_and_setup_logging
from src.comet.data.dto.moderation_dto import ModerationDTO

logger = parse_args_and_setup_logging()

openai_client = OpenAI()


def get_moderation_result(content: str) -> ModerationDTO:
    """Identify potentially harmful content in text.

    Parameters
    ----------
    content : str
        The text content to be moderated.

    Returns
    -------
    ModerationDTO
        - id (str): The unique identifier for this moderation request
        - category_scores (Dict[str, float]): Confidence scores for
          each moderation category
        - flagged (bool): Whether the content was flagged or not

    Raises
    ------
    ValueError
        If the API response cannot be parsed as JSON

    """
    moderation_result = openai_client.moderations.create(
        model="omni-moderation-latest",
        input=content,
    )

    moderation_str = model_json(moderation_result)

    try:
        moderation_json = json.loads(moderation_str)
    except json.JSONDecodeError as err:
        msg = "JSONDecodeError has occurred"
        raise ValueError(msg) from err

    moderation_result = {"id": moderation_json.get("id")}

    results = moderation_json.get("results", [])
    if results and isinstance(results, list):
        first_result = results[0]
        moderation_result["category_scores"] = first_result.get("category_scores")
        moderation_result["flagged"] = first_result.get("flagged")

    return ModerationDTO(**moderation_result)
