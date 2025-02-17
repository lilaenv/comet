from discord import app_commands


class OpenAIModelConfig:
    """Configuration class for openai models.

    Parameters
    ----------
    model : app_commands.Choice[int]
        The options of the model to be used for chat.
    max_tokens : int
        The maximum number of tokens that can be generated in the
        completion. Must be between 0 and 128000.
    temperature : float
        The temperature parameter for sampling, controlling randomness.
        Must be between 0.0 and 2.0.
    top_p : float
        The top-p sampling parameter, controlling diversity. Must be
        between 0.0 and 1.0.

    Attributes
    ----------
    model : app_commands.Choice[int]
        The options of the model.
    max_tokens : int
        The max_tokens for the chat.
    temperature : float
        The temperature parameter for sampling.
    top_p : float
        The top-p sampling parameter.

    """

    def __init__(
        self,
        model: app_commands.Choice[int],
        max_tokens: int,
        temperature: float,
        top_p: float,
    ):
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p

    @property
    def model(self) -> app_commands.Choice[int]:
        return self._model

    @model.setter
    def model(self, value: app_commands.Choice[int]) -> None:
        self._model = value

    @property
    def max_tokens(self) -> int:
        return self._max_tokens

    @max_tokens.setter
    def max_tokens(self, value: int) -> None:
        if not (0 < value <= 128000):  # noqa: PLR2004
            msg = "Invalid max_tokens value"
            raise ValueError(msg)
        self._max_tokens = value

    @property
    def temperature(self) -> float:
        return self._temperature

    @temperature.setter
    def temperature(self, value: float) -> None:
        # openai-apiのtemperatureは0.0から2.0が有効
        if not (0.0 <= value <= 2.0):  # noqa: PLR2004
            msg = "Invalid temperature value"
            raise ValueError(msg)
        self._temperature = value

    @property
    def top_p(self) -> float:
        return self._top_p

    @top_p.setter
    def top_p(self, value: float) -> None:
        if not (0.0 <= value <= 1.0):
            msg = "Invalid top_p value"
            raise ValueError(msg)
        self._top_p = value
