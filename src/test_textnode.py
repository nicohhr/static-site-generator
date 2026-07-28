import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.PLAIN_TEXT, "google.com")
        self.assertEqual("TextNode(This is a text node, plain, google.com)", repr(node))

    def test_url_none(self):
        node = TextNode("Testing None node", TextType.PLAIN_TEXT)
        self.assertEqual(node.url, None)

    def test_non_eq_type(self):
        node_1 = TextNode("Testing TextType", TextType.PLAIN_TEXT, "google.com")
        node_2 = TextNode("Testing TextType", TextType.BOLD_TEXT, "google.com")
        self.assertNotEqual(node_1, node_2)

if __name__ == "__main__":
    unittest.main()
