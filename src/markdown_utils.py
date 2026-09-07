import re

from src.htmlnode import HTMLNode
from src.parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from enum import Enum

class BlockType(Enum):
   PARAGRAPH = "paragraph"
   HEADING = "heading"
   CODE = "code"
   QUOTE = "quote"
   UNORDERED_LIST = "unordered_list"
   ORDERED_LIST = "ordered_list"

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


def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter: str,
    splited_text_type: TextType = TextType.PLAIN,
) -> list[TextNode]:

    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type == TextType.PLAIN:
            splited_text = node.text.split(delimiter)
            if len(splited_text) % 2 == 0:
                raise Exception("Error. Non closing delimiters")  # noqa: TRY002
            for i in range(len(splited_text)):
                if splited_text[i] == "":
                    continue
                if (i % 2) == 0:
                    new_nodes.append(TextNode(splited_text[i], TextType.PLAIN))
                else:
                    new_nodes.append(TextNode(splited_text[i], splited_text_type))
        else:
            new_nodes.append(node)
    return new_nodes


def extract_markdown_images(text_md: str) -> list[tuple[str, str]]:
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text_md)
    return matches


def extract_markdown_links(text_md: str) -> list[tuple[str, str]]:
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text_md)
    return matches


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type == TextType.PLAIN:
            # Extract Text
            img_match = extract_markdown_images(node.text)
            # Split
            remaining_text = node.text
            for match in img_match:
                splited_text = remaining_text.split(f"![{match[0]}]({match[1]})", 1)
                remaining_text = splited_text[1]
                if splited_text[0] != "":
                    new_nodes.append(TextNode(splited_text[0], TextType.PLAIN))
                new_nodes.append(TextNode(match[0], TextType.IMAGE, match[1]))
            if remaining_text:
                new_nodes.append(TextNode(remaining_text, TextType.PLAIN))
        else:
            new_nodes.append(node)
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type == TextType.PLAIN:
            # Extract text
            link_match = extract_markdown_links(node.text)
            # Split text
            remaining_text = node.text
            # In case there is no link
            for match in link_match:
                splited_text = remaining_text.split(f"[{match[0]}]({match[1]})", 1)
                remaining_text = splited_text[1]
                if splited_text[0] != "":
                    new_nodes.append(TextNode(splited_text[0], TextType.PLAIN))
                new_nodes.append(TextNode(match[0], TextType.LINK, match[1]))
            if remaining_text:
                new_nodes.append(TextNode(remaining_text, TextType.PLAIN))
        else:
            new_nodes.append(node)
    return new_nodes

def text_to_text_nodes(text: str) -> list[TextNode]:
    new_nodes = [TextNode(text, TextType.PLAIN)]

    # BOlD
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    # ITALIC
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    # CODE
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    # LINK
    new_nodes = split_nodes_link(new_nodes)
    # IMAGE
    new_nodes = split_nodes_image(new_nodes)

    return new_nodes

def markdown_to_blocks(text: str) -> list[str]:
    splited_block = text.split("\n\n")
    blocks: list[str] = []
    for block in splited_block:
        blocks.append(block.strip())
    return blocks

def markdown_to_html_node(markdown: str) -> HTMLNode | None:
    blocks_md = markdown_to_blocks(markdown)
    parent_node = ParentNode("md_node", [])
    for block in blocks_md:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                pass


    pass
