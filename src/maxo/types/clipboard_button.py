from maxo.enums.button_type import ButtonType
from maxo.types.button import Button


class ClipboardButton(Button):
    """
    После нажатия на кнопку указанный текст копируется в буфер обмена

    Args:
        payload: Текст, который копируется в буфер обмена после нажатия на кнопку
        type:
    """

    type: ButtonType = ButtonType.CLIPBOARD

    payload: str
    """Текст, который копируется в буфер обмена после нажатия на кнопку"""
