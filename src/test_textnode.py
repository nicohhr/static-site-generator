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

    def test_image(self):
        node = TextNode("Image description", TextType.IMAGE, "/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "/image.png", "alt": "Image description"})
        self.assertEqual(html_node.to_html(), '<img src="/image.png" alt="Image description"></img>')

    def test_link(self):
        node = TextNode("Example", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), '<a href="https://example.com">Example</a>')

if __name__ == "__main__":
    unittest.main()
