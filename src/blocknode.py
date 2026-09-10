from typing import override
from htmlnode import HTMLNode
from enum import Enum

from leafnode import LeafNode


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


class BlockNode(HTMLNode):
    def __init__(
        self,
        type: BlockType | None,
        tag: str | None = None,
        value: str | None = None,
        children: list[LeafNode] | None = None,
    ) -> None:
        super().__init__(tag, value, children, None)

    @override
    def __str__(self) -> str:
        return super().__str__()
