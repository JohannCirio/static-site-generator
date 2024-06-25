from textnode import TextNode
from htmlnode import HTMLNode
from htmlnode import LeafNode
from inline_markdown import split_nodes_delimiter

def main():

    split_test_node_1 = TextNode('Eu adoro o *Gremio* e odeio o Inter.', 'text')
    split_test_node_2 = TextNode('Eu vou comprar mutias camisetas do *Gremio* e odeio o time do Inter.', 'text')

    split_test_node_3 = TextNode('Eu adoro o **Gremio** e odeio o Inter.', 'text')
    split_test_node_4 = TextNode('Eu vou comprar mutias camisetas do **Gremio** e odeio o time do **Inter**', 'text')
    text_array = [split_test_node_1, split_test_node_2]
    text_array_2 = [split_test_node_3]
    text_array_3 = [split_test_node_4]

    result_array = split_nodes_delimiter(text_array, "*", "bold")
    result_array_2 = split_nodes_delimiter(text_array_2, "**", "italic")
    result_array_3 = split_nodes_delimiter(text_array_3, "**", "italic")
    print(result_array)
    print(result_array_2)
    print(result_array_3)


main()