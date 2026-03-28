from maxo.enums.markup_element_type import MarkupElementType
from maxo.types.markup_element import MarkupElement


# Нет в доке, работает
class HighlightedMarkup(MarkupElement):
    type: MarkupElementType = MarkupElementType.HIGHLIGHTED
