from dataclasses import dataclass

from maxo.bot.defaults import BotDefaults


@dataclass
class BotConfig:
    defaults: BotDefaults | None = None
    """Default values for bot API calls."""
