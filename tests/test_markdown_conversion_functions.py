import unittest
from src.markdown_conversion_functions import (
    parse_ordered_list,
    parse_unordered_list,
    parse_quote,
    parse_code,
    parse_headings,
)
from src.nodes_htmlnode import ParentNode, LeafNode


class TestListParsing(unittest.TestCase):
    def test_ordered_list(self):
        self.assertEqual(
            repr(
                ParentNode(
                    "ol",
                    [
                        ParentNode("li", [LeafNode(None, "item one")]),
                        ParentNode("li", [LeafNode(None, "item two")]),
                        ParentNode("li", [LeafNode(None, "item three")]),
                    ],
                )
            ),
            repr(
                ParentNode(
                    "ol", parse_ordered_list("1. item one\n2. item two\n3. item three")
                )
            ),
        )

    def test_unordered_list(self):
        self.assertEqual(
            repr(
                ParentNode(
                    "ul",
                    [
                        ParentNode("li", [LeafNode(None, "item one")]),
                        ParentNode("li", [LeafNode(None, "item two")]),
                        ParentNode("li", [LeafNode(None, "item three")]),
                    ],
                )
            ),
            repr(
                ParentNode(
                    "ul", parse_unordered_list("- item one\n* item two\n- item three")
                )
            ),
        )


class TestQuoteParsing(unittest.TestCase):
    def test_quote(self):
        self.assertEqual(
            repr(
                ParentNode(
                    "blockquote",
                    [LeafNode(None, "text goes here. some other text")],
                )
            ),
            repr(
                ParentNode(
                    "blockquote", parse_quote("> text goes here.\n> some other text")
                )
            ),
        )


class TestCodeParsing(unittest.TestCase):
    def test_code(self):
        self.assertEqual(
            repr(
                ParentNode(
                    "pre",
                    [
                        ParentNode(
                            "code",
                            [
                                LeafNode(None, "beep boop i am\nsome code\n"),
                            ],
                        )
                    ],
                )
            ),
            repr(ParentNode("pre", parse_code("```beep boop i am\nsome code\n```"))),
        )


class TestHeadingParsing(unittest.TestCase):
    def test_heading_one(self):
        self.assertEqual(
            repr(ParentNode("h1", [LeafNode(None, "this is a heading one")])),
            repr(parse_headings("# this is a heading one")),
        )

    def test_heading_two(self):
        self.assertEqual(
            repr(ParentNode("h2", [LeafNode(None, "this is a heading two")])),
            repr(parse_headings("## this is a heading two")),
        )

    def test_heading_three(self):
        self.assertEqual(
            repr(ParentNode("h3", [LeafNode(None, "this is a heading three")])),
            repr(parse_headings("### this is a heading three")),
        )

    def test_heading_four(self):
        self.assertEqual(
            repr(ParentNode("h4", [LeafNode(None, "this is a heading four")])),
            repr(parse_headings("#### this is a heading four")),
        )

    def test_heading_five(self):
        self.assertEqual(
            repr(ParentNode("h5", [LeafNode(None, "this is a heading five")])),
            repr(parse_headings("##### this is a heading five")),
        )

    def test_heading_six(self):
        self.assertEqual(
            repr(ParentNode("h6", [LeafNode(None, "this is a heading six")])),
            repr(parse_headings("###### this is a heading six")),
        )
