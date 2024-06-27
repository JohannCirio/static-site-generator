import unittest

from inline_markdown import split_nodes_delimiter
from inline_markdown import extract_markdown_images
from inline_markdown import extract_markdown_links
from inline_markdown import split_nodes_image
from inline_markdown import split_nodes_link
from inline_markdown import text_to_text_node
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

class TestNodeImageSplitter(unittest.TestCase):

    def test_one_node_img_present_middle(self):
        text = "This is text with an ![alt text](http://blabla.com/img) and more text"
        node = TextNode(text, "text")
        nodes_list = [node]

        desired_result = [
            TextNode("This is text with an ", "text"),
            TextNode("alt text", "image", "http://blabla.com/img"),
            TextNode(" and more text", "text")
        ]
    
        self.assertEqual(split_nodes_image(nodes_list), desired_result)

    def test_one_node_img_present_beginning(self):
        text = "![alt text](http://blabla.com/img) and more text"
        node = TextNode(text, "text")
        nodes_list = [node]
        
        desired_result = [
            TextNode("alt text", "image", "http://blabla.com/img"),
            TextNode(" and more text", "text")
        ]
    
        self.assertEqual(split_nodes_image(nodes_list), desired_result)

    def test_one_node_img_present_end(self):
        text = "This is text with an ![alt text](http://blabla.com/img)"
        node = TextNode(text, "text")
        nodes_list = [node]
        
        desired_result = [
            TextNode("This is text with an ", "text"),
            TextNode("alt text", "image", "http://blabla.com/img")
        ]
    
        self.assertEqual(split_nodes_image(nodes_list), desired_result)

    def test_three_nodes_img_present_middle(self):
        text = "This is text with an ![alt text](http://blabla.com/img) and more text"
        node = TextNode(text, "text")
        nodes_list = [node, node, node]

        desired_result = [
            TextNode("This is text with an ", "text"),
            TextNode("alt text", "image", "http://blabla.com/img"),
            TextNode(" and more text", "text"),
            TextNode("This is text with an ", "text"),
            TextNode("alt text", "image", "http://blabla.com/img"),
            TextNode(" and more text", "text"),
            TextNode("This is text with an ", "text"),
            TextNode("alt text", "image", "http://blabla.com/img"),
            TextNode(" and more text", "text")
        ]
    
        self.assertEqual(split_nodes_image(nodes_list), desired_result)
    
    def test_one_node_three_imgs_present_middle(self):
        text = "This is text with an ![alt text](http://blabla.com/img) and another ![text alt](http://google.com/img) and more text"
        node = TextNode(text, "text")
        nodes_list = [node]

        desired_result = [
            TextNode("This is text with an ", "text"),
            TextNode("alt text", "image", "http://blabla.com/img"),
            TextNode(" and another ", "text"),
            TextNode("text alt", "image", "http://google.com/img"),
            TextNode(" and more text", "text")
        ]
    
        self.assertEqual(split_nodes_image(nodes_list), desired_result)

    def test_one_node_three_imgs_start_middle_end(self):
        text = "![alt text](http://blabla.com/img) and another ![text alt](http://google.com/img) and another ![text alt](http://google.com/img)"
        node = TextNode(text, "text")
        nodes_list = [node]

        desired_result = [
            TextNode("alt text", "image", "http://blabla.com/img"),
            TextNode(" and another ", "text"),
            TextNode("text alt", "image", "http://google.com/img"),
            TextNode(" and another ", "text"),
            TextNode("text alt", "image", "http://google.com/img"),
        ]
    
        self.assertEqual(split_nodes_image(nodes_list), desired_result)
    
    def test_one_node_imgs_with_link(self):
        text = "![alt text](http://blabla.com/img) and another link [text alt](http://google.com/img)"
        node = TextNode(text, "text")
        nodes_list = [node]

        desired_result = [
            TextNode("alt text", "image", "http://blabla.com/img"),
            TextNode(" and another link [text alt](http://google.com/img)", "text"),
        ]
    
        self.assertEqual(split_nodes_image(nodes_list), desired_result)

class TestNodeLinkSplitter(unittest.TestCase):
    def test_one_node_link_present_middle(self):
        text = "This is text with a [link](http://blabla.com/link) and more text"
        node = TextNode(text, "text")
        nodes_list = [node]

        desired_result = [
            TextNode("This is text with a ", "text"),
            TextNode("link", "link", "http://blabla.com/link"),
            TextNode(" and more text", "text")
        ]
    
        self.assertEqual(split_nodes_link(nodes_list), desired_result)

    def test_one_node_link_present_beginning(self):
        text = "[link](http://blabla.com/link) and more text"
        node = TextNode(text, "text")
        nodes_list = [node]
        
        desired_result = [
            TextNode("link", "link", "http://blabla.com/link"),
            TextNode(" and more text", "text")
        ]
    
        self.assertEqual(split_nodes_link(nodes_list), desired_result)

    def test_one_node_link_present_end(self):
        text = "This is text with a [link](http://blabla.com/link)"
        node = TextNode(text, "text")
        nodes_list = [node]
        
        desired_result = [
            TextNode("This is text with a ", "text"),
            TextNode("link", "link", "http://blabla.com/link")
        ]
    
        self.assertEqual(split_nodes_link(nodes_list), desired_result)

    def test_three_nodes_link_present_middle(self):
        text = "This is text with a [link](http://blabla.com/link) and more text"
        node = TextNode(text, "text")
        nodes_list = [node, node, node]

        desired_result = [
            TextNode("This is text with a ", "text"),
            TextNode("link", "link", "http://blabla.com/link"),
            TextNode(" and more text", "text"),
            TextNode("This is text with a ", "text"),
            TextNode("link", "link", "http://blabla.com/link"),
            TextNode(" and more text", "text"),
            TextNode("This is text with a ", "text"),
            TextNode("link", "link", "http://blabla.com/link"),
            TextNode(" and more text", "text")
        ]
    
        self.assertEqual(split_nodes_link(nodes_list), desired_result)
    
    def test_one_node_two_links_present_middle(self):
        text = "This is text with a [link text](http://blabla.com/link) and another [another link text](http://google.com/link) and more text"
        node = TextNode(text, "text")
        nodes_list = [node]

        desired_result = [
            TextNode("This is text with a ", "text"),
            TextNode("link text", "link", "http://blabla.com/link"),
            TextNode(" and another ", "text"),
            TextNode("another link text", "link", "http://google.com/link"),
            TextNode(" and more text", "text")
        ]
    
        self.assertEqual(split_nodes_link(nodes_list), desired_result)

    def test_one_node_three_links_start_middle_end(self):
        text = "[link 1](http://blabla.com/link) and another [link 2](http://google.com/link) and another [link 3](http://google.com/link)"
        node = TextNode(text, "text")
        nodes_list = [node]

        desired_result = [
            TextNode("link 1", "link", "http://blabla.com/link"),
            TextNode(" and another ", "text"),
            TextNode("link 2", "link", "http://google.com/link"),
            TextNode(" and another ", "text"),
            TextNode("link 3", "link", "http://google.com/link"),
        ]
    
        self.assertEqual(split_nodes_link(nodes_list), desired_result)
    
    def test_one_node_link_and_img(self):
        text = "![alt text](http://blabla.com/img) and another link [link](http://google.com/link)"
        node = TextNode(text, "text")
        nodes_list = [node]

        desired_result = [
            TextNode("![alt text](http://blabla.com/img) and another link ", "text"),
            TextNode("link", "link", "http://google.com/link"),
        ]
    
        self.assertEqual(split_nodes_link(nodes_list), desired_result)

class TestTextToTextNode(unittest.TestCase):
    def test_from_boot_dev(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        desired_result = [
            TextNode("This is ", "text"),
            TextNode("text", "bold"),
            TextNode(" with an ", "text"),
            TextNode("italic", "italic"),
            TextNode(" word and a ", "text"),
            TextNode("code block", "code"),
            TextNode(" and an ", "text"),
            TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", "text"),
            TextNode("link", "link", "https://boot.dev"),
        ]

        self.assertEqual(text_to_text_node(text), desired_result)
        
