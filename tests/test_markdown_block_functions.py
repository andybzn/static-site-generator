import unittest
from src.markdown_block_functions import markdown_to_blocks, block_to_block_type


class TestMarkdownToBlocks(unittest.TestCase):
    def test_block_splitting(self):
        document = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list
* This is a list item
* This is another list item"""
        self.assertListEqual(
            markdown_to_blocks(document),
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list\n* This is a list item\n* This is another list item",
            ],
        )


class TestBlocksToBlockType(unittest.TestCase):
    def test_paragraph(self):
        self.assertEqual(block_to_block_type("paragraph"), "paragraph")

    def test_headings(self):
        self.assertEqual(block_to_block_type("# heading"), "heading")
        self.assertEqual(block_to_block_type("## heading"), "heading")
        self.assertEqual(block_to_block_type("### heading"), "heading")
        self.assertEqual(block_to_block_type("#### heading"), "heading")
        self.assertEqual(block_to_block_type("##### heading"), "heading")
        self.assertEqual(block_to_block_type("###### heading"), "heading")

    def test_code(self):
        self.assertEqual(
            block_to_block_type("```text\n\nthis is a code block\n```"), "code"
        )
        self.assertEqual(
            block_to_block_type("```\n\nthis is a code block\n```"), "code"
        )
        self.assertNotEqual(
            block_to_block_type("```\n\nthis is not a code block"), "code"
        )

    def test_quote(self):
        self.assertEqual(block_to_block_type("> quote"), "quote")
        self.assertEqual(block_to_block_type("> quote\n> quote\n> quote"), "quote")
        self.assertNotEqual(block_to_block_type("not quote"), "quote")

    def test_unordered_list(self):
        self.assertEqual(
            block_to_block_type("- item one\n- item two\n- item three"),
            "unordered_list",
        )
        self.assertEqual(
            block_to_block_type("* item one\n* item two\n* item three"),
            "unordered_list",
        )
        self.assertNotEqual(
            block_to_block_type("item one\n item two\nitem three"), "unordered_list"
        )

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. item one"), "ordered_list")
        self.assertEqual(
            block_to_block_type("1. item one\n2. item two\n3. item three"),
            "ordered_list",
        )
        self.assertNotEqual(
            block_to_block_type("- item one\n- item two\n- item three"), "ordered_list"
        )


if "__name__" == "__main__":
    unittest.main()
