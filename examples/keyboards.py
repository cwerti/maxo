import logging
import os

from magic_filter import F

from maxo import Bot, Ctx, Dispatcher, Router
from maxo.integrations.magic_filter import MagicFilter
from maxo.routing.filters import CommandStart
from maxo.routing.updates import MessageCallback, MessageCreated
from maxo.transport.long_polling import LongPolling
from maxo.utils.builders import KeyboardBuilder
from maxo.utils.facades import MessageCallbackFacade, MessageCreatedFacade

router = Router()


# KeyboardBuilder: callback, link, request_contact, request_geo_location;
# adjust - кол-во кнопок в ряд
@router.message_created(CommandStart())
async def start_handler(
    update: MessageCreated,
    ctx: Ctx,
    facade: MessageCreatedFacade,
) -> None:
    maxo_url = "https://github.com/K1rL3s/maxo"
    keyboard = (
        KeyboardBuilder()
        .add_callback(text="Колбэк", payload="click_me")
        .add_message(text="Сообщение")
        .add_link(text="Перейти в maxo", url=maxo_url)
        .add_clipboard(text="Скопировать maxo", payload=maxo_url)
        .add_request_contact(text="Поделится контактами")
        .add_request_geo_location(text="Поделится гео позицией")
        .adjust(2, 2, 1, 1)
    )

    await facade.answer_text(
        "Клавиатура",
        keyboard=keyboard.build(),
    )


@router.message_callback(MagicFilter(F.payload == "click_me"))
async def click_me_handler(
    update: MessageCallback,
    facade: MessageCallbackFacade,
) -> None:
    await facade.callback_answer("Ты кликнул на меня")


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)

    bot = Bot(os.environ["TOKEN"])
    dp = Dispatcher()
    dp.include(router)

    LongPolling(dp).run(bot)


if __name__ == "__main__":
    main()
