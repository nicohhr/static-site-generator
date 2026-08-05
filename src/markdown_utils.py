from textnode import TextNode, TextType

def split_test(old_nodes: list[TextNode], delimiter: str):
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        splited_text = node.text.split(delimiter)
        for slice in splited_text:
            new_nodes.append(TextNode(slice, TextType.PLAIN))
    return new_nodes


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode] | None:
    return None

def testing_split():
    res: list[TextNode] = []
    test_test = ["Hello World, im trying to split 'code' using a delimiter",
                "Hello World, im trying to split 'code using a delimiter'",
                "'Hello World', im trying to split code using a delimiter"]
    for test in test_test:
        res.append(TextNode(test, TextType.PLAIN))

    for tested_node in split_test(res, "'"):
        print(tested_node.text + "|")


if __name__ == "__main__":
    testing_split()
