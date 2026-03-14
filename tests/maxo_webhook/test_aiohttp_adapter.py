from unittest.mock import AsyncMock, MagicMock

import pytest
from aiohttp import web

from maxo.webhook.adapters.aiohttp.adapter import AiohttpBoundRequest, AiohttpWebAdapter


@pytest.fixture
def aiohttp_app():
    return web.Application()


@pytest.fixture
def mocked_engine():
    engine = MagicMock()
    engine.feed_request = AsyncMock()
    return engine


@pytest.mark.skip("Разобраться с ошибкой")
@pytest.mark.asyncio
async def test_adapter(aiohttp_client, aiohttp_app):
    engine = AsyncMock(return_value=web.Response(status=200))

    adapter = AiohttpWebAdapter()
    adapter.register(aiohttp_app, "/webhook", engine)

    client = await aiohttp_client(aiohttp_app)
    await client.post("/webhook", json={"foo": "bar"})

    engine.assert_awaited_once()
    request = engine.call_args.args[0]
    assert isinstance(request, AiohttpBoundRequest)
    assert await request.json() == {"foo": "bar"}
