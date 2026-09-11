import re
from enum import Enum
from typing import override

from textnode import text_node_to_html_node
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from src.markdown_utils import text_to_text_nodes
from src.textnode import text_node_to_html_node


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
        tag: str | None = None,
        children: list[LeafNode] | None = None,
    ) -> None:
        super().__init__(tag, None, children, None)

    @override
    def __str__(self) -> str:
        return super().__str__()


def block_to_block_type(input_md: str) -> BlockType:
    if re.match(r"^(#{1,6})\s+", input_md) is not None:
        return BlockType.HEADING
    if re.match(r"^(```)\n(.*)(```)", input_md):
        return BlockType.CODE
    if re.match(r"^>(.*)", input_md):
        return BlockType.QUOTE
    if re.match(r"^-\s+(.*)", input_md):
        return BlockType.UNORDERED_LIST

    # Ordered List
    numbers: list = re.findall(r"^\s*(\d+)[.)]\s+.*", input_md, re.MULTILINE)
    if len(numbers) != 0:
        for n, num in enumerate(numbers, start=1):
            if n != int(num):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def markdown_to_blocks(text: str) -> list[str]:
    splited_block = text.split("\n\n")
    blocks: list[str] = []
    for block in splited_block:
        blocks.append(block.strip())
    return blocks

def heading_to_html(input: str) -> BlockNode | None:
    # Group heading and text
    matchs = re.match(r"^\s*(#{1,6})\s+(.*)$", input)

    if matchs is not None:
        # Convert block into inline textnodes
        inline_texnodes = text_to_text_nodes(matchs.group(2))

        # Leaf node collection
        leafs: list[LeafNode] = []

        # Convert text nodes into html nodes
        for text_node in inline_texnodes:
            leafs.append(text_node_to_html_node(text_node))

        # Create Block node with inline nodes
        return BlockNode(tag=f"h{len(matchs.group(1))}", children=leafs)



def markdown_to_html_node(markdown: str) -> HTMLNode | None:
    blocks_md = markdown_to_blocks(markdown)
    parent_node = ParentNode(children=[])

    # result of each iteraction should be a COLLECTION of leafnodes
    # of the type of text
    for block in blocks_md:
        # Get the type of block
        block_type = block_to_block_type(block)
        if block_type != BlockType.CODE:

            # Creating corresponding BlockNode
            match block_type:
                case BlockType.HEADING:
                    # Relating new block to parent
                    parent_node = heading_to_html(block)

    return parent_node
