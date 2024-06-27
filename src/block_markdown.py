import re

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

def markdown_to_blocks_solution(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

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