from unittest import TestCase
from textnode import TextNode, TextType
from markdown_utils import *

class TestMarkdownUtils(TestCase):

    def test_multiple_entries(self):

        res: list[TextNode] = []
        test_test = ["Hello World, im trying to split 'code' using a delimiter",
                    "Hello World, im trying to split 'code using a delimiter'"]

        for test in test_test:
            res.append(TextNode(test, TextType.PLAIN))

        res.append(TextNode("'Hello World', im trying to split code using a delimiter", TextType.CODE))

        new_nodes = split_nodes_delimiter(res, "'", TextType.CODE)

        print(new_nodes)

    def test_split_at_start(self):
        pass
