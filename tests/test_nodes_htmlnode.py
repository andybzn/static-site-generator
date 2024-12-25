import unittest
from src.nodes_htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode(
            "a", "link", None, {"href": "https://andy.bz", "target": "_blank"}
        )
        self.assertEqual(
            "HTMLNode(a, link, children: None, {'href': 'https://andy.bz', 'target': '_blank'})",
            repr(node),
        )

    def test_props(self):
        node = HTMLNode(
            "a", "link", None, {"href": "https://andy.bz", "target": "_blank"}
        )
        self.assertEqual(
            ' href="https://andy.bz" target="_blank"', node.props_to_html()
        )

    def test_values(self):
        node = HTMLNode(
            "a", "link", None, {"href": "https://andy.bz", "target": "_blank"}
        )
        self.assertEqual("a", node.tag)
        self.assertEqual("link", node.value)
        self.assertIsNone(node.children)
        self.assertEqual({"href": "https://andy.bz", "target": "_blank"}, node.props)

    def test_class(self):
        node = HTMLNode(
            "a", "link", None, {"href": "https://andy.bz", "target": "_blank"}
        )
        self.assertIsInstance(node, HTMLNode)


class TestLeafNode(unittest.TestCase):
    def test_no_tag(self):
        node = LeafNode(None, "test text")
        self.assertEqual("test text", node.to_html())

    def test_no_value(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None).to_html()

    def test_no_props(self):
        node = LeafNode("b", "bold text")
        self.assertEqual("<b>bold text</b>", node.to_html())

    def test_with_props(self):
        node = LeafNode("a", "andy.bz", {"href": "https://andy.bz", "target": "_blank"})
        self.assertEqual(
            '<a href="https://andy.bz" target="_blank">andy.bz</a>', node.to_html()
        )

    def test_no_children(self):
        node = LeafNode("a", "andy.bz", {"href": "https://andy.bz", "target": "_blank"})
        self.assertIsNone(node.children)


class TestParentNode(unittest.TestCase):
    def test_no_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(None, "test").to_html()

    def test_no_value(self):
        with self.assertRaises(ValueError):
            ParentNode("p", None).to_html()

    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "Italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            "<p><b>Bold text</b>Normal text<i>Italic text</i>Normal text</p>",
            node.to_html(),
        )

    def test_recusive_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "Italic text"),
                LeafNode(None, "Normal text"),
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "Italic text"),
                        LeafNode(None, "Normal text"),
                    ],
                ),
            ],
        )
        self.assertEqual(
            "<p><b>Bold text</b>Normal text<i>Italic text</i>Normal text<p><b>Bold text</b>Normal text<i>Italic text</i>Normal text</p></p>",
            node.to_html(),
        )


if "__name__" == "__main__":
    unittest.main()
