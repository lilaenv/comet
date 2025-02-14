from discord import app_commands


class ModelConfig:
    """Configuration class for chat models.

    Parameters
    ----------
    model : app_commands.Choice[int]
        The options of the model to be used for chat.
    temperature : float, optional
        The temperature parameter for sampling, controlling randomness.
        Must be between 0.0 and 1.0. Defaults to 1.0.
    top_p : float, optional
        The top-p sampling parameter, controlling diversity. Must be
        between 0.0 and 1.0. Defaults to 0.5.

    Attributes
    ----------
    model : app_commands.Choice[int]
        the options of the model.
    temperature : float
        The temperature parameter for sampling.
    top_p : float
        The top-p sampling parameter.

    """

    def __init__(
        self,
        model: app_commands.Choice[int],
        temperature: float = 1.0,
        top_p: float = 0.5,
    ):
        self.model = model
        self.temperature = temperature
        self.top_p = top_p

    @property
    def model(self) -> app_commands.Choice[int]:
        return self._model

    @model.setter
    def model(self, value: app_commands.Choice[int]) -> None:
        self._model = value

    @property
    def temperature(self) -> float:
        return self._temperature

    @temperature.setter
    def temperature(self, value: float) -> None:
        if not (0.0 <= value <= 2.0):  # noqa: PLR2004
            msg = "`temperature` は 0.0 から 2.0 の間で設定してください"
            raise ValueError(msg)
        self._temperature = value

    @property
    def top_p(self) -> float:
        return self._top_p

    @top_p.setter
    def top_p(self, value: float) -> None:
        if not (0.0 <= value <= 1.0):
            msg = "`top_p` は 0.0 から 1.0 の間で設定してください"
            raise ValueError(msg)
        self._top_p = value
