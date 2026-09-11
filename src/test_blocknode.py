from pydoc import html
import unittest

from blocknode import *

class TestBlocks(unittest.TestCase):
    def test_paragraph_to_html(self):
        node = paragraph_to_html("Some **bold** text\nwith _italic_ and `code`.")
        html = node.to_html()
        print(html)
        self.assertEqual(
            html,
            "<p>Some <b>bold</b> text with <i>italic</i> and <code>code</code>.</p>",
        )

    def test_markdown_to_blocks_skips_empty_blocks(self):
        self.assertEqual(markdown_to_blocks("\n\nFirst\n\n \n\nSecond\n\n"), ["First", "Second"])

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        if node is not None:
            html = node.to_html()
            print(html)
            self.assertEqual(
                html,
                "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
            )
