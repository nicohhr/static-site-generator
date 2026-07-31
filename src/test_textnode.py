import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.PLAIN, "google.com")
        self.assertEqual("TextNode(This is a text node, plain, google.com)", repr(node))

    def test_url_none(self):
        node = TextNode("Testing None node", TextType.PLAIN)
        self.assertEqual(node.url, None)

    def test_non_eq_type(self):
        node_1 = TextNode("Testing TextType", TextType.PLAIN, "google.com")
        node_2 = TextNode("Testing TextType", TextType.BOLD, "google.com")
        self.assertNotEqual(node_1, node_2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
if __name__ == "__main__":
    unittest.main()
