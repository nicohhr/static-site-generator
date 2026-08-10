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
                raise Exception("Error. Non closing delimiters")
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
