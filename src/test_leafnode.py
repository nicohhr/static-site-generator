from unittest import TestCase
from leafnode import LeafNode

class TestLeafNode(TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_p_props(self):
        node = LeafNode("p", "Hello, world!", props={"href": "google.com", "title": "leaf_test",})
        self.assertEqual(node.to_html(), '<p href="google.com" title="leaf_test">Hello, world!</p>')

    def test_leaf_repr(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.__repr__(), "Tag: \"p\" | Value: \"Hello, world!\"| Props: \"None\"")
