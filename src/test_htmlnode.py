import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):


    def test_repr_n1(self):
        n1 = HTMLNode(tag="href", value="gmail.com", props={"node": "test_1"})
        print(repr(n1))


    def test_repr_n2(self):
        n2 = HTMLNode(tag="h1", value="Main Title", props={"n2": "test_2"})
        print(repr(n2))


    def test_repr_n3(self):
        n1 = HTMLNode(tag="href", value="gmail.com", props={"node": "test_1"})
        n2 = HTMLNode(tag="h1", value="Main Title", props={"n2": "test_2"})
        n3 = HTMLNode(tag="p", value="Something", children=[n1, n2], props={"n3": "test_2"})
        print(repr(n3))
