from textnode import TextNode

def text_node_to_html_node(text_node):
    valid_types = ["text", "bold", "italic", "code", "link", "image"]

    if text_node.text_type not in valid_types:
        raise ValueError(f"Invalid TextNode type: {text_node.text_type}")

    if text_node.text_type == "text":
        return LeafNode(tag="", value=text_node.value)
    elif text_node.text_type == "bold":
        return LeafNode(tag="b", value=text_node.value)
    elif text_node.text_type == "italic":
        return LeafNode(tag="i", value=text_node.value)
    elif text_node.text_type == "code":
        return LeafNode(tag="code", value=text_node.value)
    elif text_node.text_type == "link":
        return LeafNode(tag="a", value=text_node.value, props={'href': text_node.href})
    elif text_node.text_type == "image":
        return LeafNode(tag="img", value="", props={'src': text_node.src, 'alt': text_node.alt})


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError("This method should be overridden by subclasses")
    
    def props_to_html(self):
        props_str = ""
        for key, value in self.props.items():
            props_str += f' {key}="{value}"'
        return props_str

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value=value, props=props)

    def to_html(self):
        opening_tag = f"<{self.tag}{self.props_to_html()}>"
        closing_tag = f"</{self.tag}>"
        return opening_tag + self.value + closing_tag

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, children=children, props=props)

    def to_html(self):
        opening_tag = f"<{self.tag}{self.props_to_html()}>"
        children_html = ''.join(child.to_html() for child in self.children)
        closing_tag = f"</{self.tag}>"
        return opening_tag + children_html + closing_tag