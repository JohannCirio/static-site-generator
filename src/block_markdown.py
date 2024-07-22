import re
from htmlnode import LeafNode
from htmlnode import ParentNode
from textnode import text_node_to_html_node
from inline_markdown import text_to_text_node

def markdown_to_blocks(markdown):
    all_lines = markdown.splitlines(True)
    blocks = []

    start = 0
    end = 0
    if len(all_lines) == 0:
        return []
    
    for index in range(len(all_lines)):
        end = index
        if all_lines[index] != "\n" and index != len(all_lines) - 1:
            continue
        
        block = ""
        while start <= end:
            if all_lines[start] != "\n":
                block += all_lines[start]
            start += 1

        clean_block = block.strip()
        if len(clean_block) != 0:
            blocks.append(clean_block)
        start = index
    return blocks

def block_to_block_type(block):
    if is_header(block):
        return "heading"
    if is_code(block):
        return "code"
    if is_quote(block):
        return "quote"
    if is_unordered_list(block):
        return "unordered_list"
    if is_ordered_list(block):
        return "ordered_list"

    return "paragraph"

def is_header(text):
    pattern = r'^#{1,6}\s+\S'
    return bool(re.match(pattern, text))

def is_code(text):
    if len(text) < 6:
        return False
    
    for char in text[:2]:
        if char != "`":
            return False
    
    for char in text[-3:]:
        if char != "`":
            return False
    
    return True

def is_quote(text):
    return all(line[0] == ">" for line in text.splitlines())

def is_unordered_list(text):
    if not text.strip():
        return False
    pattern = r'^[\*\-] '
    return all(bool(re.match(pattern, line)) for line in text.splitlines())

def is_ordered_list(text):
    all_lines =  text.splitlines()
    for index in range(len(all_lines)):
        if len(all_lines[index]) < 4:
            return False
        
        if (all_lines[index][0] != str(index + 1)) or (all_lines[index][1] != ".") or (all_lines[index][2] != " "):
            return False
    
    return True


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []

    for block in blocks:
        
        block_type = block_to_block_type(block)
        print(block)
        print(block_type)
        html_node = block_to_htmlnode(block, block_type)
        html_nodes.append(html_node)

    main_node = ParentNode(children=html_nodes, tag="div")
    return main_node

def block_to_htmlnode(block, type):
    if type == "heading":
        return heading_to_html(block)
    elif type == "code":
        return code_to_html(block)
    elif type == "quote":
        return quote_to_html(block)
    elif type == "unordered_list":
        return unordered_list_to_html(block)
    elif type == "ordered_list":
        return ordered_list_to_html(block)
    elif type == "paragraph":
        return paragraph_to_html(block)
    else:
        raise Exception("No type")


def paragraph_to_html(block):
    text_nodes = text_to_text_node(block)
    leaf_nodes = list(map(text_node_to_html_node, text_nodes))
    parent_node = ParentNode(children=leaf_nodes, tag="p")
    return parent_node

def heading_to_html(block):
    heading_level = 0
    for char in block:
        if char == "#":
            heading_level += 1
        else:
            break
    
    tag = f"h{str(heading_level)}"
    
    text_nodes = text_to_text_node(block[heading_level + 1:])
    leaf_nodes = list(map(text_node_to_html_node, text_nodes))
    
    parent_node = ParentNode(children=leaf_nodes, tag=tag)
    return parent_node

def code_to_html(block):
    # removes the code block ```
    text_nodes = text_to_text_node(block[3:-3])
    leaf_nodes = list(map(text_node_to_html_node, text_nodes))

    code_html_node = ParentNode(children=leaf_nodes, tag="code")
    pre_html_node = ParentNode(children=[code_html_node], tag="pre")
    return pre_html_node

def quote_to_html(block):
    list_lines = block.splitlines()
    new_list_lines = []

    for line in list_lines:
        new_list_lines.append(line[2:])

    text = "\n".join(new_list_lines)
    text_nodes = text_to_text_node(text)
    leaf_nodes = list(map(text_node_to_html_node, text_nodes))

    quote_html_node = ParentNode(children=leaf_nodes, tag="blockquote")
    return quote_html_node

def ordered_list_to_html(block):
    list_lines = block.splitlines()
    text_nodes_by_line = []

    for item in list_lines:
        text_nodes = text_to_text_node(item[3:])
        leaf_nodes = list(map(text_node_to_html_node, text_nodes))
        text_nodes_by_line.append(leaf_nodes)

    li_leafs_list = []
    for text_nodes in text_nodes_by_line:
        li_leafs_list.append(ParentNode(children=text_nodes, tag="li"))
    
    ol_node = ParentNode(children=li_leafs_list, tag="ol")
    return ol_node

def unordered_list_to_html(block):
    list_lines = block.splitlines()
    text_nodes_by_line = []

    for item in list_lines:
        text_nodes = text_to_text_node(item[2:])
        leaf_nodes = list(map(text_node_to_html_node, text_nodes))
        text_nodes_by_line.append(leaf_nodes)

    li_leafs_list = []
    for text_nodes in text_nodes_by_line:
        li_leafs_list.append(ParentNode(children=text_nodes, tag="li"))
    
    ul_node = ParentNode(children=li_leafs_list, tag="ul")
    return ul_node


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    pattern = r'^#\s+\S'
    for block in blocks:
        if bool(re.match(pattern, block)):
            text = block[1:].strip()
            return text
    raise Exception("There is no main title in this markdown text.")