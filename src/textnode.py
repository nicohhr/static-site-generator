from enum import Enum
from typing import override


class TextType(Enum):
    PLAIN_TEXT = "plain"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINK_TEXT = "link"
    IMAGE_TEXT = "image"
    BOLD_TEXT = "bold"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text: str = text
        self.text_type: TextType = text_type
        self.url: str | None = url

    @override
    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, TextNode):
            return False

        return(self.text == value.text
            and self.text_type == value.text_type
            and self.url == value.url)

    @override
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
