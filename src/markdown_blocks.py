import os

from htmlnode import ParentNode, text_node_to_html_node, LeafNode
from inline_markdown import text_to_textnodes

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_olist = "ordered_list"
block_type_ulist = "unordered_list"

def block_to_block_type(block):
    lines = block.split("\n")

    if (
        block.startswith("# ")
        or block.startswith("## ")
        or block.startswith("### ")
        or block.startswith("#### ")
        or block.startswith("##### ")
        or block.startswith("###### ")
    ):
        return block_type_heading
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return block_type_code
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return block_type_paragraph
        return block_type_quote
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return block_type_paragraph
        return block_type_ulist
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return block_type_paragraph
        return block_type_ulist
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return block_type_paragraph
            i += 1
        return block_type_olist
    return block_type_paragraph

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown) 
    children = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", children)

markdown_content = "# Tolkien Fan Club\nSome more content\n* item1\n* item2"
html_node = markdown_to_html_node(markdown_content)
print(html_node.to_html())


def block_to_html_node(block):
    if block.startswith("# "):
        return LeafNode("h1", block[2:].strip())
    elif block.startswith("## "):
        return LeafNode("h2", block[3:].strip())
    elif block.startswith("* "):
        items = block.split('\n* ')[1:]
        return ParentNode("ul", [LeafNode("li", item) for item in items])
    elif block.startswith("> "):
        return LeafNode("blockquote", block[2:].strip())
    else:
        return LeafNode("p", block.strip())

markdown_content = "# Tolkien Fan Club\nSome more content\n* item1\n* item2"
html_node = markdown_to_html_node(markdown_content)
print(html_node.to_html())

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
    


def markdown_to_blocks(markdown):
    return markdown.split('\n\n')  # Simple split by double newline

def extract_title(markdown):
    for line in markdown.split('\n'):
        if line.startswith('# '):
            return line[2:].strip()
    raise ValueError("No H1 title found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    if not os.path.exists(template_path):
        print(f"Error: Template file does not exist at '{template_path}'")
        return

    with open(from_path, 'r') as f:
        markdown_content = f.read()

    with open(template_path, 'r') as f:
        template_content = f.read()

    dest_directory = os.path.dirname(dest_path)
    if not os.path.exists(dest_directory):
        os.makedirs(dest_directory)

    html_content = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)

    full_html = template_content.replace('{{ Title }}', title).replace('{{ Content }}', html_content)

    with open(dest_path, 'w') as f:
        f.write(full_html)

