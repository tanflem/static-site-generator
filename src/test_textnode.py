import unittest

from textnode import TextNode
from htmlnode import LeafNode, ParentNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"
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

    def test_text_to_text_nodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        nodes = TextNode.text_to_text_nodes(text)
        nodes_test = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]

        self.assertEqual(nodes, nodes_test)

    def test_markdown_to_blocks(self):
        markdown = "   This is a markdown\n\nblock"
        blocks = TextNode.markdown_to_blocks(markdown)
        blocks_test = ["This is a markdown", "block"]
        self.assertEqual(blocks, blocks_test)

    def test_markdown_to_blocks_empty(self):
        markdown = f"This is **bolded** paragraph\n\nThis is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line\n\n* This is a list\n* with items\n"
        blocks = TextNode.markdown_to_blocks(markdown)
        blocks_test = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items",
        ]
        self.assertEqual(blocks, blocks_test)

    def test_markdown_to_html_node(self):
        markdown = "This is **bolded** paragraph\n\n# heading 1\n\n## heading 2 with **bold**\n\nThis is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line\n\n* This is a list\n* with items\n\n```This is a code block```\n\n> This is a blockquote with [link](https://boot.dev) and an ![image](https://i.imgur.com/zjjcJKZ.png\n\n* This is a task\n* This is a completed task\n\n1. This is a numbered list\n2. with items\n\nThis is a paragraph with a [link](https://boot.dev) and an ![image](https://i.imgur.com/zjjcJKZ.png)"
        nodes = TextNode.markdown_to_html_node(markdown)
       
        # self.assertEqual(nodes, nodes_test)

if __name__ == "__main__":
    unittest.main()
