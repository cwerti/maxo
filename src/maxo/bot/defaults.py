from dataclasses import dataclass

from maxo.enums import TextFormat


@dataclass
class BotDefaults:
    """Default values for bot API calls."""

    text_format: TextFormat | None = None
    """Default text format for messages"""
    disable_link_preview: bool | None = None
    """Default value for disable_link_preview parameter"""
