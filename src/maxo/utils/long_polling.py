# ruff: noqa: E501

import warnings

from maxo.transport.long_polling import LongPolling

warnings.warn(
    "`LongPolling` был перенесён из `maxo.utils.long_polling` в `maxo.transport.long_polling`. "
    "Пожалуйста, обновите импорты на 'from maxo.transport.long_polling import LongPolling'",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ("LongPolling",)
