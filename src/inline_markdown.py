import re
from textnode import TextNode

def text_to_text_node(text):
    text_nodes = [TextNode(text, 'text')]
    text_nodes = split_nodes_delimiter(text_nodes, "**", 'bold')
    text_nodes = split_nodes_delimiter(text_nodes, "*", 'italic')
    text_nodes = split_nodes_delimiter(text_nodes, "`", 'code')
    text_nodes = split_nodes_link(text_nodes)
    text_nodes = split_nodes_image(text_nodes)
    
    return text_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        found_images = extract_markdown_images(node.text)
        
        if node.text_type != 'text':
            new_nodes.append(node)
            continue
        
        if len(found_images) == 0:
            new_nodes.append(node)
            continue
        
        node_text = node.text
        for img in found_images:
            split_text = node_text.split(f"![{img[0]}]({img[1]})", 1)
            
            if split_text[0] != "":
                new_nodes.append(TextNode(split_text[0], 'text'))
            
            new_nodes.append(TextNode(img[0], "image", img[1]))
            node_text = split_text[1]
        
        if node_text != "":
            new_nodes.append(TextNode(node_text, "text"))
    
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        found_links = extract_markdown_links(node.text)
        
        if node.text_type != 'text':
            new_nodes.append(node)
            continue

        if len(found_links) == 0:
            new_nodes.append(node)
            continue
        
        node_text = node.text
        for link in found_links:
            split_text = node_text.split(f"[{link[0]}]({link[1]})", 1)
            
            if split_text[0] != "":
                new_nodes.append(TextNode(split_text[0], 'text'))
            
            new_nodes.append(TextNode(link[0], "link", link[1]))
            node_text = split_text[1]
        
        if node_text != "":
            new_nodes.append(TextNode(node_text, "text"))
    
    return new_nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    final_list = []
    for node in old_nodes:
        final_list += one_node_spliter(node, delimiter, text_type)
    return final_list

def one_node_spliter(node, delimiter, text_type):
    new_nodes_list = []
    old_nodes = [node]
    
    if node.text_type != 'text':
        return old_nodes
    
    start_position = find_delimiter(node.text, delimiter)

    if start_position == -1:
        return old_nodes
    
    if start_position == len(node.text):
        raise Exception("Closing Limiter not found, invalid Markdown Syntax")

    end_position = node.text.find(delimiter, start_position + len(delimiter))

    if end_position == -1:
        raise Exception("Closing Limiter not found, invalid Markdown Syntax")

    # skip creating text node when delimitter is on the start of text
    if start_position != 0:
        new_nodes_list.append(TextNode(node.text[:start_position], "text"))

    new_nodes_list.append(TextNode(node.text[start_position + len(delimiter):end_position], text_type))

    if node.text[end_position + len(delimiter):] != "":
        new_nodes_list.append(TextNode(node.text[end_position + len(delimiter):], 'text'))


    if (len(old_nodes) == len(new_nodes_list)) or (new_nodes_list[-1].text_type != 'text'): 
        return new_nodes_list
    else:
        final_list = new_nodes_list[:-1] + one_node_spliter(new_nodes_list[-1], delimiter, text_type)
        return final_list

def find_delimiter(text, delimiter):
    start_position = text.find(delimiter)

    if start_position == -1:
        return start_position
    
    try:
        while text[start_position + 1] == delimiter:
                start_position = text.find(delimiter, start_position + 2)
    except IndexError:
        raise Exception("Closing Limiter not found, invalid Markdown Syntax")

    return start_position