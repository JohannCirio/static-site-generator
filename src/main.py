from textnode import TextNode
from htmlnode import HTMLNode
from htmlnode import LeafNode
from inline_markdown import split_nodes_delimiter
from inline_markdown import extract_markdown_images
from inline_markdown import extract_markdown_links
from block_markdown import markdown_to_blocks
from block_markdown import block_to_block_type

def main():
    text = "```  ```"
    text1 = "``````"
    text2 = "```    sdasda ```2"
    text3 = "``` dasdas ```"
    text12 = ">line\n>line\n>line22"
    print(block_to_block_type(text2))
    print(block_to_block_type(text12))

main()