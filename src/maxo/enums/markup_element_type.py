from enum import StrEnum


# У клиента есть QUOTE (цитата), но в доке не описана и боту не приходит
# https://t.me/maxo_py/671
class MarkupElementType(StrEnum):
    EMPHASIZED = "emphasized"
    LINK = "link"
    MONOSPACED = "monospaced"
    STRIKETHROUGH = "strikethrough"
    STRONG = "strong"
    UNDERLINE = "underline"
    USER_MENTION = "user_mention"
    QUOTE = "quote"  # Нет в доке, работает
    HEADING = "heading"  # Нет в доке, работает
    HIGHLIGHTED = "highlighted"  # Нет в доке, работает
