import unittest

from inline_markdown import split_nodes_delimiter
from inline_markdown import extract_markdown_images
from inline_markdown import extract_markdown_links
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
        text_node_2 = TextNode("Eu `serei` o grande `campeao` desta `copa`", "text")
        text_list = [text_node, text_node_2]
    
        desired_result = [
            TextNode("Eu ", "text"),
            TextNode("serei", "code"),
            TextNode(" o grande ", "text"),
            TextNode("campeao", "code"),
            TextNode(" desta ", "text"),
            TextNode("copa", "code"),
            TextNode("Eu ", "text"),
            TextNode("serei", "code"),
            TextNode(" o grande ", "text"),
            TextNode("campeao", "code"),
            TextNode(" desta ", "text"),
            TextNode("copa", "code"),
        ]
        self.assertEqual(split_nodes_delimiter(text_list, "`", "code"), desired_result)

    def test_invalid_code_end(self):
        text_node = TextNode("Eu `serei` o grande `campeao` desta `copa", "text")
        text_list = [text_node]

        with self.assertRaises(Exception) as context: 
            result = split_nodes_delimiter(text_list, "`", 'code')

        self.assertEqual(str(context.exception), "Closing Limiter not found, invalid Markdown Syntax")

    def test_invalid_code_middle(self):
        text_node = TextNode("Eu `serei o grande `campeao` desta `copa`", "text")
        text_list = [text_node]

        with self.assertRaises(Exception) as context: 
            result = split_nodes_delimiter(text_list, "`", 'code')

        self.assertEqual(str(context.exception), "Closing Limiter not found, invalid Markdown Syntax")
    
    def test_invalid_bold_with_italic(self):
        text_node = TextNode("Eu *serei o grande* **campeao** desta copa**", "text")
        text_list = [text_node]

        with self.assertRaises(Exception) as context: 
            result = split_nodes_delimiter(text_list, "**", 'bold')

        self.assertEqual(str(context.exception), "Closing Limiter not found, invalid Markdown Syntax")

class TestImageExtractor(unittest.TestCase):
    def test_one_img_present(self):
        text = "This is text with an ![alt text](http://blabla.com/img)"
        desired_result = [("alt text", "http://blabla.com/img")]
    
        self.assertEqual(extract_markdown_images(text), desired_result)
    
    def test_two_imgs_present(self):
        text = "This is text with an ![alt text](http://blabla.com/img) and another one ![text alt](http://gremio.com/img)"
        desired_result = [("alt text", "http://blabla.com/img"), ("text alt", "http://gremio.com/img")]
    
        self.assertEqual(extract_markdown_images(text), desired_result)

    def test_no_img(self):
        text = "This is text with no img"
        desired_result = []
    
        self.assertEqual(extract_markdown_images(text), desired_result)

    def test_with_link(self):
        text = "This is text with link [link](http://blabla.com/img)"
        desired_result = []
    
        self.assertEqual(extract_markdown_images(text), desired_result)

    def test_with_link_and_img(self):
        text = "This is text with link [link](http://blabla.com/img) and img ![alt text](http://blabla.com/img)"
        desired_result = [("alt text", "http://blabla.com/img")]
    
        self.assertEqual(extract_markdown_images(text), desired_result)


    class TestLinkExtractor(unittest.TestCase):
        def test_one_link_present(self):
            text = "This is text with an [link](http://blabla.com/img)"
            desired_result = [("link", "http://blabla.com/img")]
        
            self.assertEqual(extract_markdown_links(text), desired_result)
        
        def test_two_links_present(self):
            text = "This is text with an [link 1](http://blabla.com/img) and another one [link 2](http://gremio.com/img)"
            desired_result = [("link 1", "http://blabla.com/img"), ("link 2", "http://gremio.com/img")]
        
            self.assertEqual(extract_markdown_links(text), desired_result)

        def test_no_link(self):
            text = "This is text with no link"
            desired_result = []
        
            self.assertEqual(extract_markdown_links(text), desired_result)

        def test_with_img(self):
            text = "This is text with link ![alt text](http://blabla.com/img)"
            desired_result = []
        
            self.assertEqual(extract_markdown_links(text), desired_result)

        def test_with_link_and_img(self):
            text = "This is text with link [link](http://blabla.com/img) and img ![alt text](http://blabla.com/img)"
            desired_result = [("link", "http://blabla.com/link")]
        
            self.assertEqual(extract_markdown_links(text), desired_result)

