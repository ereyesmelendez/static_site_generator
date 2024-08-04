from textnode import TextNode

def text_node_to_html_node(text_node):
    valid_types = ["text", "bold", "italic", "code", "link", "image"]

    if text_node.type not in valid valid_types:
        raise ValueError(f"Invalid TextNode type: {text_node.type}")

    if text_node.type == "text":
        return LeafNode(tag="", value=text_node.value)
    elif text_node.type == "bold":
        return LeafNode(tag="b", value=text_node.value)
    elif text_node.type == "italic":
        return LeafNode(tag="i", value=text_node.value)
    elif text_node.type == "code":
        return LeafNode(tag="code", value=text_node.value)
    elif text_node.type == "link":
        return LeafNode(tag="a", value=text_node.value, href=text_node.href)
    elif text_node.type == "image":
        return LeafNode(tag="img", value="", src=text_node.src, alt=text_node.alt)


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else{}

    def to_html(self):
        raise NotImplementatedError("This method should be overriden by subclasses")
    
    def props_to_html(self):
        props_str = ""
        for key, value in self.props.items():
            props_str += f' {key}="{value}"'
        return props_str

    def __repr__(self):
        return f"HTMNode(tag={self.tag}, value{self.value}, children={self.children}, props{self.props})"

    class LeafNode(HTMLNode):
        def __init__(self, tag, value, attributes=None):
            super(self).__init__(tag, attributes)
            self.value = value
            if self.value is None:
                raise ValueError("LeafNode must have a value")

    class ParentNode(HTMLNode):
        def __init__(self, tag, children):
            self.tag = tag
            self.children = children
            if self.tag is None:
                raise ValueError("ParentNode must have a tag")
            if not self.children:
                raise ValueError("ParentNode must have children")
        def to_html(self):
            opening_tag = f"<{self.tag}>"

            children_html = ''.Join(child.to_html() for child in self.children)

            closing_tag = f"<{self.tag}>"

            return opening_tag + children_html + closing_tag