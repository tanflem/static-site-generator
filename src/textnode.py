from htmlnode import LeafNode
import re

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__ (self, target):
        return self.text == target.text and self.text_type == target.text_type and self.url == target.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
    def text_node_to_html_node(self):
        if self.text_type == text_type_text:
            return LeafNode(value = self.text)
        elif self.text_type == text_type_bold:
            return LeafNode(tag = "b", value = self.text)
        elif self.text_type == text_type_italic:
            return LeafNode(tag = "i", value = self.text)
        elif self.text_type == text_type_code:
            return LeafNode(tag = "code", value = self.text)
        elif self.text_type == text_type_link:
            return LeafNode(tag = "a", value = self.text, props = {"href": self.url})
        elif self.text_type == text_type_image:
            return LeafNode(tag = "img", value = self.text, props = {"src": self.url})
        else:
            raise Exception(f"Invalid text type: {self.text_type}")
        
    def split_nodes_delimiter(old_nodes, delimiter, text_type):
        new_nodes = []
        for node in old_nodes:
            # If the node is text, split on the delimiter
            if node.text_type == text_type_text:
                # Raise exception if the delimiter is not closed
                delimiter_count = node.text.count(delimiter)
                if delimiter_count % 2 != 0:
                    raise Exception(f"Missing closing delimiter: {delimiter} in {node.text}")

                # Split the text on the delimiter
                split_nodes = node.text.split(delimiter)
                # If the text is inside a delimiter, add the text as a text_type node
                # else add it as a text node
                for i, split_node in enumerate(split_nodes):
                    if split_node == "":
                        continue
                    if i % 2 == 0:
                        new_nodes.append(TextNode(split_node, text_type_text))
                    else:
                        new_nodes.append(TextNode(split_node, text_type))

            # If the node is not text, add it to the new nodes
            else:
                new_nodes.append(node)
        return new_nodes
    
    def extract_markdown_images(text):
        return re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    
    def extract_markdown_links(text):
        return re.findall(r"\[(.*?)\]\((.*?)\)", text)
    
    def split_nodes_image(old_nodes):
        new_nodes = []
        print("\n")
        print(f"OLD NODES: {old_nodes}")
        for node in old_nodes:
            images = TextNode.extract_markdown_images(node.text)
            if len(images) == 0:
                new_nodes.append(node)
                continue
            # Large string here
            # For each image in the node text, 
            temp_text = node.text
            for image_tup in images:
                node_split_on_image = temp_text.split(f"![{image_tup[0]}]({image_tup[1]})", 1)
                if node_split_on_image[0] != "":
                    new_nodes.append(TextNode(node_split_on_image[0], text_type_text))
                new_nodes.append(TextNode(image_tup[0], text_type_image, image_tup[1]))
                temp_text = node_split_on_image[1]
                if temp_text != "" and images.index(image_tup) == len(images) - 1:
                    new_nodes.append(TextNode(temp_text, text_type_text))
        for node in new_nodes:
            print(f"NEW NODE: {node}")
        print("\n")
        return new_nodes
    
    def split_nodes_link(old_nodes):
        new_nodes = []
        for node in old_nodes:
            links = TextNode.extract_markdown_links(node.text)
            if len(links) == 0:
                new_nodes.append(node)
                continue
            # Large string here
            # For each link in the node text, 
            temp_text = node.text
            for link_tup in links:
                node_split_on_link = temp_text.split(f"[{link_tup[0]}]({link_tup[1]})", 1)
                if node_split_on_link[0] != "":
                    new_nodes.append(TextNode(node_split_on_link[0], text_type_text))
                new_nodes.append(TextNode(link_tup[0], text_type_link, link_tup[1]))
                temp_text = node_split_on_link[1]
                if temp_text != "" and links.index(link_tup) == len(links) - 1:
                    new_nodes.append(TextNode(temp_text, text_type_text))
        return new_nodes