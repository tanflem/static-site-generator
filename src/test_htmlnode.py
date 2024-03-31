import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("div", "This is a text node")
        node2 = HTMLNode("div", "This is a text node")
        self.assertEqual(node.__repr__(), node2.__repr__())

    def test_props_to_html(self):
        node = HTMLNode("div", "This is a text node", props={"class": "text"})
        self.assertEqual(node.props_to_html(), ' class="text"')
        node = HTMLNode("div", "This is a text node", props={"class": "text", "id": "text"})
        self.assertEqual(node.props_to_html(), ' class="text" id="text"')

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("div", "This is a text node")
        self.assertEqual(node.to_html(), "<div>This is a text node</div>")
        node = LeafNode(None, "This is a text node")
        self.assertEqual(node.to_html(), "This is a text node")
        node = LeafNode("div", "This is a text node", props={"class": "text"})
        self.assertEqual(node.to_html(), '<div class="text">This is a text node</div>')
        node = LeafNode(None, None, None)
        self.assertRaises(ValueError, node.to_html)
class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node1 = ParentNode("div", [LeafNode(None, "This is a text node")])
        self.assertEqual(node1.to_html(), "<div>This is a text node</div>")

        node2 = ParentNode(
            "p",
            children=[
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node2.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )
        node3 = ParentNode("div", None, props={"class": "text"})
        self.assertRaises(ValueError, node3.to_html)

        node4 = ParentNode(None, [LeafNode(None, "This is a text node")], None)
        self.assertRaises(ValueError, node4.to_html)


if __name__ == "__main__":
    unittest.main()
