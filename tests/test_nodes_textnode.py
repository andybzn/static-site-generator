import unittest
from src.nodes_textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("This is a link node", TextType.LINK, "http://andy.bz")
        self.assertIsNotNone(node.url)

    def test_url_eq(self):
        node = TextNode("This is a link node", TextType.LINK, "http://andy.bz")
        node2 = TextNode("This is a link node", TextType.LINK, "http://andy.bz")
        self.assertEqual(node, node2)

    def test_text_type(self):
        node = TextNode("Test text_types", TextType.TEXT)
        self.assertIsInstance(node.text_type, TextType)

    def test_class(self):
        node = TextNode("This is an instance of a TextNode", TextType.TEXT)
        self.assertIsInstance(node, TextNode)

    def test_repr(self):
        node = TextNode("This is a link node", TextType.LINK, "http://andy.bz")
        self.assertEqual(
            "TextNode(This is a link node, link, http://andy.bz)", repr(node)
        )

    # this set of tests checks conversion from TextNode to LeafNode
    def test_conversion_invalid(self):
        with self.assertRaises(ValueError):
            text_node_to_html_node(TextNode("p", "Something"))

    def test_conversion_normal(self):
        node = text_node_to_html_node(TextNode("I am just plain text", TextType.TEXT))
        self.assertEqual("LeafNode(None, I am just plain text, None)", repr(node))

    def test_conversion_bold(self):
        node = text_node_to_html_node(TextNode("I am some bold text", TextType.BOLD))
        self.assertEqual("LeafNode(b, I am some bold text, None)", repr(node))

    def test_conversion_italic(self):
        node = text_node_to_html_node(
            TextNode("I am some italic text", TextType.ITALIC)
        )
        self.assertEqual("LeafNode(i, I am some italic text, None)", repr(node))

    def test_conversion_code(self):
        node = text_node_to_html_node(TextNode("I am some 1337 code", TextType.CODE))
        self.assertEqual("LeafNode(code, I am some 1337 code, None)", repr(node))

    def test_conversion_url(self):
        node = text_node_to_html_node(
            TextNode("I am an URL!", TextType.LINK, "http://andy.bz")
        )
        self.assertEqual(
            "LeafNode(a, I am an URL!, {'href': 'http://andy.bz'})", repr(node)
        )

    def test_conversion_image(self):
        node = text_node_to_html_node(
            TextNode("I am an image!", TextType.IMAGE, "http://andy.bz/test.png")
        )
        self.assertEqual(
            "LeafNode(img, , {'src': 'http://andy.bz/test.png', 'alt': 'I am an image!'})",
            repr(node),
        )


if "__name__" == "__main__":
    unittest.main()
