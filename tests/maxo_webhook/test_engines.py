from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from maxo.bot.bot import Bot
from maxo.routing.dispatcher import Dispatcher
from maxo.routing.signals import (
    AfterShutdown,
    AfterStartup,
    BeforeShutdown,
    BeforeStartup,
)
from maxo.webhook.engines.simple import SimpleEngine
from maxo.webhook.engines.token import TokenEngine


class TestSimpleEngine:
    @pytest.fixture
    def dispatcher(self) -> Dispatcher:
        return Dispatcher()

    @pytest.fixture
    def bot(self) -> MagicMock:
        return MagicMock(spec=Bot)

    @pytest.fixture
    def web_adapter(self) -> MagicMock:
        return MagicMock()

    @pytest.fixture
    def routing(self) -> MagicMock:
        return MagicMock()

    @pytest.fixture
    def security(self) -> MagicMock:
        security = MagicMock()
        security.get_secret_token = AsyncMock(return_value="secret")
        return security

    @pytest.fixture
    def engine(
        self,
        dispatcher: Dispatcher,
        bot: MagicMock,
        web_adapter: MagicMock,
        routing: MagicMock,
        security: MagicMock,
    ) -> SimpleEngine:
        return SimpleEngine(
            dispatcher,
            bot,
            web_adapter=web_adapter,
            routing=routing,
            security=security,
        )

    def test_get_bot_from_request(self, engine: SimpleEngine, bot: MagicMock):
        assert engine._get_bot_from_request(MagicMock()) is bot

    @pytest.mark.asyncio
    async def test_set_webhook(
        self,
        engine: SimpleEngine,
        bot: MagicMock,
        routing: MagicMock,
    ):
        routing.webhook_point.return_value = "https://example.com/webhook"
        bot.subscribe = AsyncMock()

        await engine.set_webhook(
            update_types=["message"],
        )

        bot.subscribe.assert_called_once()
        call_kwargs = bot.subscribe.call_args.kwargs
        assert call_kwargs["url"] == "https://example.com/webhook"
        assert call_kwargs["update_types"] == ["message"]

    @pytest.mark.asyncio
    async def test_on_startup(self, engine: SimpleEngine, dispatcher: Dispatcher):
        dispatcher.feed_signal = AsyncMock()
        await engine.on_startup(app=MagicMock())
        assert dispatcher.feed_signal.await_count == 2
        assert isinstance(
            dispatcher.feed_signal.await_args_list[0].args[0],
            BeforeStartup,
        )
        assert isinstance(
            dispatcher.feed_signal.await_args_list[1].args[0],
            AfterStartup,
        )

    @pytest.mark.asyncio
    async def test_on_shutdown(
        self,
        engine: SimpleEngine,
        dispatcher: Dispatcher,
        bot: MagicMock,
    ):
        dispatcher.feed_signal = AsyncMock()
        bot.close = AsyncMock()
        await engine.on_shutdown(app=MagicMock())
        assert dispatcher.feed_signal.await_count == 2
        bot.close.assert_awaited_once()
        assert isinstance(
            dispatcher.feed_signal.await_args_list[0].args[0],
            BeforeShutdown,
        )
        assert isinstance(
            dispatcher.feed_signal.await_args_list[1].args[0],
            AfterShutdown,
        )


class TestTokenEngine:
    @pytest.fixture
    def dispatcher(self) -> Dispatcher:
        return Dispatcher()

    @pytest.fixture
    def web_adapter(self) -> MagicMock:
        return MagicMock()

    @pytest.fixture
    def routing(self) -> MagicMock:
        routing = MagicMock()
        routing.extract_token.return_value = "42:TEST"
        return routing

    @pytest.fixture
    def security(self) -> MagicMock:
        security = MagicMock()
        security.get_secret_token = AsyncMock(return_value="secret")
        return security

    @pytest.fixture
    def engine(
        self,
        dispatcher: Dispatcher,
        web_adapter: MagicMock,
        routing: MagicMock,
        security: MagicMock,
    ) -> TokenEngine:
        return TokenEngine(
            dispatcher,
            web_adapter=web_adapter,
            routing=routing,
            security=security,
        )

    def test_get_bot(self, engine: TokenEngine):
        with patch("maxo.webhook.engines.token.Bot") as bot_mock:
            bot_mock.side_effect = [MagicMock(spec=Bot), MagicMock(spec=Bot)]

            bot1 = engine.get_bot("42:TEST")
            bot2 = engine.get_bot("42:TEST")
            bot3 = engine.get_bot("43:TEST")

            assert bot1 is bot2
            assert bot1 is not bot3
            bot_mock.assert_any_call(token="42:TEST", defaults=None)  # noqa: S106
            bot_mock.assert_any_call(token="43:TEST", defaults=None)  # noqa: S106
            assert bot_mock.call_count == 2

    def test_get_bot_from_request(self, engine: TokenEngine):
        with patch.object(engine, "get_bot") as get_bot_mock:
            engine._get_bot_from_request(MagicMock())
            get_bot_mock.assert_called_once_with("42:TEST")

    @pytest.mark.asyncio
    async def test_set_webhook(self, engine: TokenEngine, routing: MagicMock):
        routing.webhook_point.return_value = "https://example.com/webhook/42:TEST"

        with patch.object(engine, "get_bot") as get_bot_mock:
            bot_mock = get_bot_mock.return_value
            bot_mock.subscribe = AsyncMock()

            await engine.set_webhook(
                "42:TEST",
                update_types=["message"],
            )

            get_bot_mock.assert_called_once_with("42:TEST")
            bot_mock.subscribe.assert_called_once()
            call_kwargs = bot_mock.subscribe.call_args.kwargs
            assert call_kwargs["url"] == "https://example.com/webhook/42:TEST"
            assert call_kwargs["update_types"] == ["message"]

    @pytest.mark.asyncio
    async def test_on_startup(self, engine: TokenEngine, dispatcher: Dispatcher):
        dispatcher.feed_signal = AsyncMock()
        await engine.on_startup(app=MagicMock())
        assert dispatcher.feed_signal.await_count == 2
        assert isinstance(
            dispatcher.feed_signal.await_args_list[0].args[0],
            BeforeStartup,
        )
        assert isinstance(
            dispatcher.feed_signal.await_args_list[1].args[0],
            AfterStartup,
        )

    @pytest.mark.asyncio
    async def test_on_shutdown(self, engine: TokenEngine, dispatcher: Dispatcher):
        with patch.object(engine, "get_bot") as get_bot_mock:
            bot_mock = get_bot_mock.return_value
            bot_mock.close = AsyncMock()
            engine._bots["42:TEST"] = bot_mock

            dispatcher.feed_signal = AsyncMock()
            await engine.on_shutdown(app=MagicMock())
            assert dispatcher.feed_signal.await_count == 2
            bot_mock.close.assert_awaited_once()
            assert not engine._bots
            assert isinstance(
                dispatcher.feed_signal.await_args_list[0].args[0],
                BeforeShutdown,
            )
            assert isinstance(
                dispatcher.feed_signal.await_args_list[1].args[0],
                AfterShutdown,
            )
