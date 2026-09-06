import unittest

from markdown_utils import *
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.PLAIN
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.PLAIN),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.PLAIN
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.PLAIN),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_extract_images(self):

        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        res = extract_markdown_images(text)
        self.assertEqual(
            res,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_images_empty(self):

        text = ""
        res = extract_markdown_images(text)
        self.assertEqual(res, [])

    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        res = extract_markdown_links(text)
        self.assertEqual(extract_markdown_links(text), res)

    def test_image_in_url(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        res = extract_markdown_links(text)
        self.assertEqual(res, [])

    def test_url_in_image(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        res = extract_markdown_images(text)
        self.assertEqual(res, [])

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_after(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) text after.",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" text after.", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_split_images_before(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) text after.",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        # print(new_nodes)
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" text after.", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "this is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])

        self.assertEqual(
            new_nodes,
            [
                TextNode("this is text with a link ", TextType.PLAIN),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.PLAIN),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
        )

    def test_split_links_after(self):
        node = TextNode(
            "this is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev), text after.",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])

        self.assertEqual(
            new_nodes,
            [
                TextNode("this is text with a link ", TextType.PLAIN),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.PLAIN),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
                TextNode(", text after.", TextType.PLAIN),
            ],
        )

    def test_split_links_before(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev), text after.",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])

        self.assertEqual(
            new_nodes,
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.PLAIN),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
                TextNode(", text after.", TextType.PLAIN),
            ],
        )

    def test_full_split(self):
        input_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_text_nodes(input_text)

        # for node in new_nodes: print(node)

        self.assertEqual(new_nodes,
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.PLAIN),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )

    def test_markdown_to_blocks_list(self):
        intput_text =   """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
        """
        # print()
        # for item in markdown_to_blocks(intput_text): print(item)

        self.assertEqual(
            markdown_to_blocks(intput_text),
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_heading_to_type_space(self):
        input = "# normal triple heading"
        res: BlockType = block_to_block_type(input)

        self.assertEqual(
            res, BlockType.HEADING
        )

    def test_heading_to_type_non_space(self):
        input = "#normal triple heading"
        res: BlockType = block_to_block_type(input)

        self.assertEqual(
            res, BlockType.PARAGRAPH
        )

    def test_code_to_type(self):
        input = "```\nif var == True: return True```"

        res: BlockType = block_to_block_type(input)
        self.assertEqual(res, BlockType.CODE)

    def test_code_to_type_bad_syntaxys(self):
        input = "```\nif var == True: return True``"

        res: BlockType = block_to_block_type(input)
        self.assertEqual(res, BlockType.PARAGRAPH)

    def test_code_to_type_non_line(self):
        input = "```if var == True: return True```"

        res: BlockType = block_to_block_type(input)
        self.assertEqual(res, BlockType.PARAGRAPH)

    def test_quote_to_type(self):
        input = "> Dorothy followed her through many of the beautiful rooms in her castle."
        res: BlockType = block_to_block_type(input)

        self.assertEqual(res, BlockType.QUOTE)

    def test_quote_to_type_non_space(self):
        input = ">Dorothy followed her through many of the beautiful rooms in her castle."
        res: BlockType = block_to_block_type(input)

        self.assertEqual(res, BlockType.QUOTE)

    def test_unordered_to_type(self):
        input = "- Dorothy followed\n - Second item"
        res: BlockType = block_to_block_type(input)

        self.assertEqual(res, BlockType.UNORDERED_LIST)

    def test_unordered_to_type_bad(self):
        input = "-Dorothy followed\n - Second item"
        res: BlockType = block_to_block_type(input)

        self.assertEqual(res, BlockType.PARAGRAPH)

    def test_ordered_list(self):
        input = """
1. First item
2. Second item
3. Third item
4. Fourth item
"""
        res: BlockType = block_to_block_type(input)
        self.assertEqual(res, BlockType.ORDERED_LIST)

    def test_ordered_list_bad(self):
        input = """
1. First item
2. Second item
4. Third item
4. Fourth item
"""
        res: BlockType = block_to_block_type(input)
        self.assertEqual(res, BlockType.PARAGRAPH)
if __name__ == "__main__":
    unittest.main()
