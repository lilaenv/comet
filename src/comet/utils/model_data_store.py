from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.comet.config.anthropic_model import AnthropicModelConfig
    from src.comet.config.openai_model import OpenAIModelConfig


class ModelDataStore:
    _instance = None
    data: dict

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.data = {}
        return cls._instance

    def set_model_config(self, key: int, config: AnthropicModelConfig | OpenAIModelConfig) -> None:
        self.data[key] = config

    def get_model_config(self, key: int) -> Any | None:  # noqa: ANN401
        return self.data.get(key)
