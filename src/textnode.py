from htmlnode import LeafNode, ParentNode
import re

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

# Define constants for each block type
BLOCK_TYPE_PARAGRAPH = "paragraph"
BLOCK_TYPE_HEADING = "heading"
BLOCK_TYPE_CODE = "code"
BLOCK_TYPE_QUOTE = "quote"
BLOCK_TYPE_UNORDERED_LIST = "unordered_list"
BLOCK_TYPE_ORDERED_LIST = "ordered_list"

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
    
    
    def text_to_text_nodes(text):
        # Split the text into nodes based on the markdown syntax
        nodes = [TextNode(text, text_type_text)]
        nodes = TextNode.split_nodes_delimiter(nodes, "**", text_type_bold)
        nodes = TextNode.split_nodes_delimiter(nodes, "*", text_type_italic)
        nodes = TextNode.split_nodes_delimiter(nodes, "`", text_type_code)
        nodes = TextNode.split_nodes_image(nodes)
        nodes = TextNode.split_nodes_link(nodes)
        return nodes
    

    def markdown_to_blocks(markdown):        
        blocks = markdown.split("\n\n")
        new_blocks = []
        for block in blocks:
            if block != "":
                new_blocks.append(block.strip())
        
        return new_blocks
    
    def block_to_block_type(block):
        # Check if the block is a heading
        if re.match(r"^#{1,6} .+", block):
            return BLOCK_TYPE_HEADING

        # Check if the block is a code block
        if block.startswith('```') and block.endswith('```'):
            return BLOCK_TYPE_CODE

        # Check if the block is a quote
        if all(line.startswith(">") for line in block.split("\n")):
            return BLOCK_TYPE_QUOTE

        # Check if the block is an unordered list
        if all(re.match(r"^(\*|-) .+", line) for line in block.split("\n")):
            return BLOCK_TYPE_UNORDERED_LIST

        # Check if the block is an ordered list
        if all(re.match(r"^\d+\. .+", line) for line in block.split("\n")):
            lines = block.split("\n")
            for i in range(len(lines)):
                if not lines[i].startswith(f"{i+1}. "):
                    return BLOCK_TYPE_PARAGRAPH
            return BLOCK_TYPE_ORDERED_LIST

        # If none of the above conditions are met, the block is a paragraph
        return BLOCK_TYPE_PARAGRAPH
    
    def block_type_paragraph_to_html_node(block):
        nodes = TextNode.text_to_text_nodes(block)
        html_nodes = [node.text_node_to_html_node() for node in nodes]
        return ParentNode(tag = "p", children = html_nodes)
    
    def block_type_heading_to_html_node(block):
        level = len(block.split(" ")[0])
        text = block[level + 1:]
        nodes = TextNode.text_to_text_nodes(text)
        html_nodes = [node.text_node_to_html_node() for node in nodes]
        return ParentNode(tag = f"h{level}", children = html_nodes)
    
    def block_type_code_to_html_node(block):
        code = block[3:-3]
        nodes = TextNode.text_to_text_nodes(code)
        html_nodes = [node.text_node_to_html_node() for node in nodes]
        return ParentNode(tag = "pre", children = [ParentNode(tag = "code", children = html_nodes)])

    def block_type_quote_to_html_node(block):
        lines = block.split("\n")
        lines = [line[1:] for line in lines]
        nodes = [TextNode(line, text_type_text) for line in lines]
        html_nodes = [node.text_node_to_html_node() for node in nodes]
        return ParentNode(tag = "blockquote", children = html_nodes)
    
    def block_type_unordered_list_to_html_node(block):
        lines = block.split("\n")
        lines = [line[2:] for line in lines]
        nodes = [TextNode(line, text_type_text) for line in lines]
        html_nodes = [ParentNode(tag = "li", children = [node.text_node_to_html_node()]) for node in nodes]
        return ParentNode(tag = "ul", children = html_nodes)

    def block_type_ordered_list_to_html_node(block):
        lines = block.split("\n")
        lines = [line[3:] for line in lines]
        nodes = [TextNode(line, text_type_text) for line in lines]
        html_nodes = [ParentNode(tag = "li", children = [node.text_node_to_html_node()]) for node in nodes]
        return ParentNode(tag = "ol", children = html_nodes)
    
    def markdown_to_html_node(markdown):
        print("\n")
        blocks = TextNode.markdown_to_blocks(markdown)
        print(blocks)
        block_with_type = [(block, TextNode.block_to_block_type(block)) for block in blocks]
        print()
        print(block_with_type)
        print()
        html_nodes = []
        for block, block_type in block_with_type:
            print(block_type)
            print(block)
            print()
            if block_type == BLOCK_TYPE_HEADING:
                print(TextNode.block_type_heading_to_html_node(block).to_html())
                print()
                html_nodes.append(TextNode.block_type_heading_to_html_node(block))
            elif block_type == BLOCK_TYPE_CODE:
                print(TextNode.block_type_code_to_html_node(block).to_html())
                print()
                html_nodes.append(TextNode.block_type_code_to_html_node(block))
            elif block_type == BLOCK_TYPE_QUOTE:
                print(TextNode.block_type_quote_to_html_node(block).to_html())
                print()
                html_nodes.append(TextNode.block_type_quote_to_html_node(block))
            elif block_type == BLOCK_TYPE_UNORDERED_LIST:
                print(TextNode.block_type_unordered_list_to_html_node(block).to_html())
                print()
                html_nodes.append(TextNode.block_type_unordered_list_to_html_node(block))
            elif block_type == BLOCK_TYPE_ORDERED_LIST:
                print(TextNode.block_type_ordered_list_to_html_node(block).to_html())
                print()
                html_nodes.append(TextNode.block_type_ordered_list_to_html_node(block))
            else:
                print(TextNode.block_type_paragraph_to_html_node(block).to_html())
                print()
                html_nodes.append(TextNode.block_type_paragraph_to_html_node(block))
        
        parent_div = ParentNode(tag = "div", children=html_nodes)
        print(parent_div.to_html())