import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):


    def test_repr(self):
        n1 = HTMLNode(tag="href", value="gmail.com", props={"node": "test_1"})
        self.assertEqual(repr(n1), "Tag: href\n" +
            "Value: gmail.com\n" +
            "Children: None\n" +
            "Props: {'node': 'test_1'}\n")

    def test_repr_n3(self):
        n1 = HTMLNode(tag="href", value="gmail.com", props={"node": "test_1"})
        n2 = HTMLNode(tag="h1", value="Main Title", props={"n2": "test_2"})
        n3 = HTMLNode(tag="p", value="Something", children=[n1, n2], props={"n3": "test_2"})
        self.assertEqual(repr(n3), "Tag: p\n" +
            "Value: Something\n" +
            "Children: [Tag: href\n" +
            "Value: gmail.com\n" +
            "Children: None\n" +
            "Props: {'node': 'test_1'}\n" +
            ", Tag: h1\n" +
            "Value: Main Title\n" +
            "Children: None\n" +
            "Props: {'n2': 'test_2'}\n" +
            "]\n" +
            "Props: {'n3': 'test_2'}\n")

    def test_instance_values(self):
        n1 = HTMLNode(tag="href", value="gmail.com", props={"node": "test_1"})

        self.assertEqual(n1.tag, "href")
        self.assertEqual(n1.value, "gmail.com")
        self.assertEqual(n1.children, None)
        self.assertEqual(n1.props, {"node": "test_1"})
