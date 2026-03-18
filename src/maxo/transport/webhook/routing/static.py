from maxo import Bot
from maxo.transport.webhook.routing.base import BaseRouting


class StaticRouting(BaseRouting):
    """Routing without token, static webhook URL."""

    def __init__(self, url: str) -> None:
        super().__init__(url=url)
        self.url_template = self.url.human_repr()

    def webhook_point(self, bot: Bot) -> str:
        return self.url_template
