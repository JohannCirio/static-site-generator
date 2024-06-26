from textnode import TextNode
from htmlnode import HTMLNode
from htmlnode import LeafNode
from inline_markdown import split_nodes_delimiter
from images_markdown import extract_markdown_images
from images_markdown import extract_markdown_links

def main():
    text_with_img = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
    text_without_img = 'This is text'
    text_with_img = "This is text with an [image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"

    extract_markdown_images(text_with_img)
    print(extract_markdown_images(text_without_img))
    print(extract_markdown_links(text_with_img))

main()