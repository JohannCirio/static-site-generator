from textnode import TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes_list = []
    for node in old_nodes:
        if node.text_type != 'text':
            new_nodes_list.append(node)
            continue
        
        start_position = find_delimiter(node.text, delimiter)

        if start_position == -1:
            new_nodes_list.append(node)
            continue

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
        final_list = new_nodes_list[:-1] + split_nodes_delimiter([new_nodes_list[-1]], delimiter, text_type)
        return final_list


def find_delimiter(text, delimiter):
    start_position = text.find(delimiter)

    if start_position == -1:
        return start_position

   
    while text[start_position + 1] == delimiter:
            start_position = text.find(delimiter, start_position + 2)
       
    return start_position