import unittest

from textnode import TextNode
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_text_node_to_html_node_bold(self):
        text_node = TextNode("This is a text node", "bold")
        leaf_node = text_node.text_node_to_html_node()
        leaf_node_test = LeafNode(tag = "b", value = "This is a text node")
        self.assertEqual(leaf_node, leaf_node_test)

    def test_text_node_to_html_node_link(self):
        text_node = TextNode("This is a link", "link", "https://www.google.com")
        leaf_node = text_node.text_node_to_html_node()
        leaf_node_test = LeafNode(tag = "a", value = "This is a link", props = {"href": "https://www.google.com"})
        self.assertEqual(leaf_node, leaf_node_test)

    def test_text_node_to_html_node_image(self):
        text_node = TextNode("This is an image", "image", "https://www.google.com")
        leaf_node = text_node.text_node_to_html_node()
        leaf_node_test = LeafNode(tag = "img", value = "This is an image", props = {"src": "https://www.google.com"})
        self.assertEqual(leaf_node, leaf_node_test)
    
    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", "text")
        new_nodes = TextNode.split_nodes_delimiter([node], "`", "code")
        new_nodes_test = [TextNode("This is text with a ", "text"), TextNode("code block", "code"), TextNode(" word", "text")]
        self.assertEqual(new_nodes, new_nodes_test)

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is `text` with a **bold word**", "text")
        new_nodes = TextNode.split_nodes_delimiter([node], "**", "bold")
        new_nodes_test = [TextNode("This is `text` with a ", "text"), TextNode("bold word", "bold")]
        self.assertEqual(new_nodes, new_nodes_test)

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("*Italic word*", "text")
        new_nodes = TextNode.split_nodes_delimiter([node], "*", "italic")
        new_nodes_test = [TextNode("Italic word", "italic")]
        self.assertEqual(new_nodes, new_nodes_test)
    
    def test_extract_markdown_images(self):
        text = "This is a text with ![image](https://www.google.com)"
        images = TextNode.extract_markdown_images(text)
        images_test = [('image', 'https://www.google.com')]
        self.assertEqual(images, images_test)
    
    def test_extract_markdown_images_multiple(self):
        text = "This is a text with ![image](https://www.google.com) and ![image2](https://www.google.com)"
        images = TextNode.extract_markdown_images(text)
        images_test = [('image', 'https://www.google.com'), ('image2', 'https://www.google.com')]
        self.assertEqual(images, images_test)

    def test_extract_markdown_images_no_images(self):
        text = "This is a text with no images"
        images = TextNode.extract_markdown_images(text)
        images_test = []
        self.assertEqual(images, images_test)
    
    def test_extract_markdown_links(self):
        text = "This is a text with [link](https://www.google.com)"
        links = TextNode.extract_markdown_links(text)
        links_test = [('link', 'https://www.google.com')]
        self.assertEqual(links, links_test)
    
    def test_extract_markdown_links_multiple(self):
        text = "This is a text with [link](https://www.google.com) and [link2](https://www.google.com)"
        links = TextNode.extract_markdown_links(text)
        links_test = [('link', 'https://www.google.com'), ('link2', 'https://www.google.com')]
        self.assertEqual(links, links_test)
    
    def test_extract_markdown_links_no_links(self):
        text = "This is a text with no links"
        links = TextNode.extract_markdown_links(text)
        links_test = []
        self.assertEqual(links, links_test)

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            "text",
        )
        new_nodes = TextNode.split_nodes_image([node])

        new_nodes_test = [
            TextNode("This is text with an ", "text"),
            TextNode("image", "image", "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", "text"),
            TextNode(
                "second image", "image", "https://i.imgur.com/3elNhQu.png"
            ),
        ]
        self.assertEqual(new_nodes, new_nodes_test)

    def test_split_nodes_image_no_images(self):
        node = TextNode("This is text with no images", "text")
        new_nodes = TextNode.split_nodes_image([node])
        new_nodes_test = [TextNode("This is text with no images", "text")]
        self.assertEqual(new_nodes, new_nodes_test)

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a [link](https://www.google.com) and another [second link](https://www.google.com)",
            "text",
        )
        new_nodes = TextNode.split_nodes_link([node])

        new_nodes_test = [
            TextNode("This is text with a ", "text"),
            TextNode("link", "link", "https://www.google.com"),
            TextNode(" and another ", "text"),
            TextNode(
                "second link", "link", "https://www.google.com"
            ),
        ]
        self.assertEqual(new_nodes, new_nodes_test)



if __name__ == "__main__":
    unittest.main()
