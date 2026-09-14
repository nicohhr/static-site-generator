import unittest

from blocknode import *


class TestBlocks(unittest.TestCase):
    def test_paragraph_to_html(self):
        node = paragraph_to_html("Some **bold** text\nwith _italic_ and `code`.")
        html = node.to_html()
        # print(html)
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
            # print(html)
            self.assertEqual(
                html,
                "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
            )

    def test_quote(self):
        md = """
> This is a **bold** quote
> across multiple lines
"""

        node = markdown_to_html_node(md)
        if node is None:
            self.fail("Expected a root HTML node")
        self.assertEqual(
            node.to_html(),
            "<div><blockquote>This is a <b>bold</b> quote across multiple lines</blockquote></div>",
        )

    def test_code(self):
        md = """
```
input = "text"

for char in input:
    print(char + "n")
```
"""

        node = markdown_to_html_node(md)
        if node is not None:
            html = node.to_html()
            self.assertEqual(
                html,
                '<div><pre><code>input = "text"\n\nfor char in input:\n    print(char + "n")\n</code></pre></div>',
            )
    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        if node is not None:
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
            )

    def test_unorderedlist_block(self):
        md="""
- item 1
- item 2
- item 3
- item n
- item n + 1
"""
        node = markdown_to_html_node(md)
        if node is not None: print(node.to_html())
