from block_markdown import markdown_to_html_node
from block_markdown import extract_title
import os
import shutil

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = open(from_path).read()
    template_html = open(template_path).read()
    html_node = markdown_to_html_node(markdown)
    converted_html_string = html_node.to_html()
    title = extract_title(markdown)

    final_html = template_html.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", converted_html_string)

    
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    
    with open(dest_path, 'w') as file:
            file.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dir_path_content) or not os.path.exists(template_path):
        raise Exception("The paths are broken")
    
    paths = os.listdir(dir_path_content)

    for path in paths:
        full_path = os.path.join(dir_path_content, path)
        
        if os.path.isfile(full_path):
            generate_page(full_path, template_path, os.path.join(dest_dir_path, "index.html"))
        else:
            destination_full_path = os.path.join(dest_dir_path, path)
            generate_pages_recursive(full_path, template_path, destination_full_path)
