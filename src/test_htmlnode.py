import unittest

from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()
