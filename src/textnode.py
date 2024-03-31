from htmlnode import LeafNode

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
       