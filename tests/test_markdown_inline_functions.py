import unittest
from src.markdown_inline_functions import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from src.nodes_textnode import TextNode, TextType


class TestMarkdownFormatting(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_multi_bold(self):
        node = TextNode(
            "This is text with a **bold** word, and another **bold word**!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word, and another ", TextType.TEXT),
                TextNode("bold word", TextType.BOLD),
                TextNode("!", TextType.TEXT),
            ],
        )

    def test_multi_italic(self):
        node = TextNode(
            "This is text with an *italic* word, and another *italic word*!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word, and another ", TextType.TEXT),
                TextNode("italic word", TextType.ITALIC),
                TextNode("!", TextType.TEXT),
            ],
        )

    def test_bold_italic(self):
        node = TextNode(
            "**bold** and *italic*",
            TextType.TEXT,
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
        )


class TestExtraction(unittest.TestCase):
    def test_images(self):
        text = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        images = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertListEqual(text, images)

    def test_urls(self):
        text = extract_markdown_links(
            "This is text with a link to [my site](https://andy.bz) and [mastodon](https://hachyderm.io/@bzn)"
        )
        urls = [
            ("my site", "https://andy.bz"),
            ("mastodon", "https://hachyderm.io/@bzn"),
        ]
        self.assertListEqual(text, urls)


class TestNodeMediaSplits(unittest.TestCase):
    def test_image_split(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/fJRm4Vk.jpeg) in it",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" in it", TextType.TEXT),
            ],
        )

    def test_image_solo(self):
        node = TextNode(
            "![image](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_multi_image_split(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/fJRm4Vk.jpeg) in it, and also another ![image](https://i.imgur.com/aKaOqIh.gif)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" in it, and also another ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            ],
        )

    def test_link_split(self):
        node = TextNode(
            "This is text with a [link](https://andy.bz) in it",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://andy.bz"),
                TextNode(" in it", TextType.TEXT),
            ],
        )

    def test_link_solo(self):
        node = TextNode(
            "[link](https://andy.bz)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("link", TextType.LINK, "https://andy.bz"),
            ],
        )


class TestFullExtraction(unittest.TestCase):
    def test_full_split(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )


if "__name__" == "__main__":
    unittest.main()
