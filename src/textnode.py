from enum import Enum
from typing import override

from leafnode import LeafNode


class TextType(Enum):
    PLAIN = "plain"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    BOLD = "bold"


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

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.PLAIN:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, props={"href": ""})
        case TextType.IMAGE:
            return LeafNode("img", props={"src": "", "alt": ""})
        case _:
            raise Exception("TextType not implemented.")
