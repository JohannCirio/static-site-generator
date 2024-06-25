import unittest

from inline_markdown import split_nodes_delimiter
from textnode import TextNode

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_text_italic_middle(self):
        text_node = TextNode("Eu serei o *grande* campeao.", "text")
        text_list = [text_node]
    
        desired_result = [
            TextNode("Eu serei o ", "text"),
            TextNode("grande", "italic"),
            TextNode(" campeao.", "text")
        ]
        self.assertEqual(split_nodes_delimiter(text_list, "*", "italic"), desired_result)

    def test_text_italic_start(self):
        text_node = TextNode("*Eu* serei o grande campeao.", "text")
        text_list = [text_node]
    
        desired_result = [
            TextNode("Eu", "italic"),
            TextNode(" serei o grande campeao.", "text"),
        ]
        self.assertEqual(split_nodes_delimiter(text_list, "*", "italic"), desired_result)

    def test_text_italic_end(self):
        text_node = TextNode("Eu serei o grande *campeao*", "text")
        text_list = [text_node]
    
        desired_result = [
            TextNode("Eu serei o grande ", "text"),
            TextNode("campeao", "italic")
        ]
        self.assertEqual(split_nodes_delimiter(text_list, "*", "italic"), desired_result)

    def test_two_text_italic_middle_n_end(self):
        text_node = TextNode("Eu serei o *grande* *campeao*", "text")
        text_list = [text_node]
    
        desired_result = [
            TextNode("Eu serei o ", "text"),
            TextNode("grande", "italic"),
            TextNode(" ", "text"),
            TextNode("campeao", "italic")
        ]
        self.assertEqual(split_nodes_delimiter(text_list, "*", "italic"), desired_result)

    def test_text_bold_end(self):
        text_node = TextNode("Eu serei o grande **campeao**", "text")
        text_list = [text_node]
    
        desired_result = [
            TextNode("Eu serei o grande ", "text"),
            TextNode("campeao", "bold")
        ]
        self.assertEqual(split_nodes_delimiter(text_list, "**", "bold"), desired_result)

    def test_text_italic_on_bold_end(self):
        text_node = TextNode("Eu serei o grande **campeao**", "text")
        text_list = [text_node]
    
        desired_result = [
            TextNode("Eu serei o grande **campeao**", "text"),
        ]
        bla = split_nodes_delimiter(text_list, "*", "bold")
        self.assertEqual(bla, desired_result)

    def test_text_bold_end(self):
        text_node = TextNode("Eu serei o grande **campeao**", "text")
        text_list = [text_node]
    
        desired_result = [
            TextNode("Eu serei o grande ", "text"),
            TextNode("campeao", "bold")
        ]
        self.assertEqual(split_nodes_delimiter(text_list, "**", "bold"), desired_result)
    
    def test_bold_plus_italic(self):
        text_node = TextNode("Eu serei o grande **campeao** desta *copa*!", "text")
        text_list = [text_node]
    
        desired_result = [
            TextNode("Eu serei o grande **campeao** desta ", "text"),
            TextNode("copa", "italic"),
            TextNode("!", 'text')
        ]
        self.assertEqual(split_nodes_delimiter(text_list, "*", "italic"), desired_result)


    def test_bold_plus_italic_end(self):
        text_node = TextNode("Eu serei o grande **campeao** desta *copa*", "text")
        text_list = [text_node]
    
        desired_result = [
            TextNode("Eu serei o grande **campeao** desta ", "text"),
            TextNode("copa", "italic")
        ]
        self.assertEqual(split_nodes_delimiter(text_list, "*", "italic"), desired_result)

    def test_code_middle(self):
        text_node = TextNode("Eu serei o grande `campeao` desta copa", "text")
        text_list = [text_node]
    
        desired_result = [
            TextNode("Eu serei o grande ", "text"),
            TextNode("campeao", "code"),
            TextNode(" desta copa", "text")
        ]
        self.assertEqual(split_nodes_delimiter(text_list, "`", "code"), desired_result)
    
    def test_multiple_codes(self):
        text_node = TextNode("Eu `serei` o grande `campeao` desta `copa`", "text")
        text_list = [text_node]
    
        desired_result = [
            TextNode("Eu ", "text"),
            TextNode("serei", "code"),
            TextNode(" o grande ", "text"),
            TextNode("campeao", "code"),
            TextNode(" desta ", "text"),
            TextNode("copa", "code")
        ]
        self.assertEqual(split_nodes_delimiter(text_list, "`", "code"), desired_result)
    
    def test_text_with_multiple_codes(self):
        text_node = TextNode("Eu `serei` o grande `campeao` desta `copa`", "text")
        text_node_2 = TextNode("Eu serei", "text")
        text_list = [text_node, text_node_2]
    
        desired_result = [
            TextNode("Eu ", "text"),
            TextNode("serei", "code"),
            TextNode(" o grande ", "text"),
            TextNode("campeao", "code"),
            TextNode(" desta ", "text"),
            TextNode("copa", "code"),
            TextNode('Eu serei', 'text')
    
        ]
        self.assertEqual(split_nodes_delimiter(text_list, "`", "code"), desired_result)