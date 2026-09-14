import re
from enum import Enum

from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from src.markdown_utils import text_to_text_nodes
from textnode import *


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


class BlockNode(ParentNode):
    def __init__(
        self,
        tag: str | None = None,
        children: list | None = None,
    ) -> None:
        super().__init__(tag=tag, children=children)

    # @override
    # def to_html(self) -> str:
    #     # Final representation
    #     f_repr = ""
    #     if self.children is not None:
    #         for children in self.children:
    #             f_repr += children.to_html()
    #     return f_repr

def block_to_block_type(input_md: str) -> BlockType:
    if re.match(r"^(#{1,6})\s+", input_md) is not None:
        return BlockType.HEADING
    if re.match(r"^```\n.*```$", input_md, re.DOTALL) is not None:
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
    blocks: list[str] = []
    parts = re.split(r"(```.*?```)", text, flags=re.DOTALL)

    for part in parts:
        if not part.strip():
            continue

        if re.fullmatch(r"```.*?```", part.strip(), flags=re.DOTALL):
            blocks.append(part.strip())
        else:
            for block in part.split("\n\n"):
                if block.strip():
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


def paragraph_to_html(input: str) -> BlockNode:
    text = input.replace("\n", " ")
    inline_textnodes = text_to_text_nodes(text)
    leafs: list[LeafNode] = []
    for text_node in inline_textnodes:
        leafs.append(text_node_to_html_node(text_node))
    return BlockNode(tag="p", children=leafs)

def code_to_html(input: str) -> BlockNode:
    code = input[4:-3]
    code_node = LeafNode(tag="code", value=code)
    return BlockNode(tag="pre", children=[code_node])

def quote_to_html(input: str) -> BlockNode:
    text = " ".join(re.sub(r"^>\s?", "", line) for line in input.splitlines())
    inline_textnodes = text_to_text_nodes(text)
    leafs: list[LeafNode] = []
    for text_node in inline_textnodes:
        leafs.append(text_node_to_html_node(text_node))
    return BlockNode(tag="blockquote", children=leafs)

def markdown_to_html_node(markdown: str) -> HTMLNode | None:
    blocks_md = markdown_to_blocks(markdown)
    parent_node = ParentNode(tag="div", children=[])

    # result of each iteraction should be a COLLECTION of leafnodes
    # of the type of text
    for block in blocks_md:
        # Get the type of block
        block_type = block_to_block_type(block)

        # Creating corresponding BlockNode
        match block_type:
            case BlockType.HEADING:
                if parent_node.children is not None:
                    parent_node.children.append(heading_to_html(block))

            case BlockType.PARAGRAPH:
                if parent_node.children is not None:
                    parent_node.children.append(paragraph_to_html(block))

            case BlockType.CODE:
                if parent_node.children is not None:
                    parent_node.children.append(code_to_html(block))

            case BlockType.QUOTE:
                if parent_node.children is not None:
                    parent_node.children.append(quote_to_html(block))

    return parent_node
