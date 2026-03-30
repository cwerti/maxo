from adaptix.load_error import LoadError
from unihttp.http import HTTPResponse
from unihttp.serialize import ResponseLoader

from maxo import loggers
from maxo.bot.methods.base import MaxoMethod
from maxo.bot.methods.markers import Query
from maxo.omit import Omittable, Omitted
from maxo.routing.updates.updates import Updates
from maxo.types.update_list import UpdateList


class GetUpdates(MaxoMethod[UpdateList], slots=False):
    """
    Получение обновлений

    Этот метод можно использовать для получения обновлений при разработке и тестировании, если ваш бот не подписан на Webhook. Для production-окружения рекомендуем использовать Webhook 

     Метод использует долгий опрос (long polling). Каждое обновление имеет свой номер последовательности. Свойство `marker` в ответе указывает на следующее ожидаемое обновление.

    Все предыдущие обновления считаются завершёнными после прохождения параметра `marker`. Если параметр `marker` **не передан**, бот получит все обновления, произошедшие после последнего подтверждения

    Пример запроса:
    ```bash
    curl -X GET "https://platform-api.max.ru/updates" \
      -H "Authorization: {access_token}"
    ```

    Args:
        limit: Максимальное количество обновлений для получения
        marker: Если передан, бот получит обновления, которые еще не были получены. Если не передан, получит все новые обновления
        timeout: Тайм-аут в секундах для долгого опроса
        types: Список типов обновлений, которые бот хочет получить (например, `message_created`, `message_callback`)

    Источник: https://dev.max.ru/docs-api/methods/GET/updates
    """

    __url__ = "updates"
    __method__ = "get"

    limit: Query[Omittable[int]] = Omitted()
    """Максимальное количество обновлений для получения"""
    marker: Query[Omittable[int | None]] = Omitted()
    """Если передан, бот получит обновления, которые еще не были получены. Если не передан, получит все новые обновления"""
    timeout: Query[Omittable[int]] = Omitted()
    """Тайм-аут в секундах для долгого опроса"""
    types: Query[Omittable[list[str] | None]] = Omitted()
    """Список типов обновлений, которые бот хочет получить (например, `message_created`, `message_callback`)"""

    def make_response(
        self,
        response: HTTPResponse,
        response_loader: ResponseLoader,
    ) -> UpdateList:
        try:
            return super().make_response(response, response_loader)
        except LoadError:
            raw = response.data
            marker = raw.get("marker")
            updates = []
            for raw_upd in raw.get("updates", []):
                try:
                    updates.append(response_loader.load(raw_upd, Updates))
                except LoadError:
                    loggers.methods.warning(
                        "Пропуск незагружаемого апдейта. Сообщите об этой ошибке в "
                        "https://github.com/K1rL3s/maxo/issues. Тело апдейта: %s",
                        raw_upd,
                        exc_info=True,
                    )
            return UpdateList(updates=updates, marker=marker)
