import re
from textnode import TextNode

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

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