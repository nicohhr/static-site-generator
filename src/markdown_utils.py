import re

from textnode import TextNode, TextType


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
