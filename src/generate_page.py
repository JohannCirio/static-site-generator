from block_markdown import markdown_to_html_node
from block_markdown import extract_title
import os

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
