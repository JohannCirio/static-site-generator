import unittest
from block_markdown import markdown_to_blocks
from block_markdown import markdown_to_blocks_solution
from block_markdown import block_to_block_type

class TestMarkdownToBlocks(unittest.TestCase):
    def test_2_normal_blocks(self):
        text = """Line 1

Line 2
Line 3"""
        desired_result = [
            "Line 1",
            "Line 2\nLine 3",
            
        ]
        self.assertEqual(markdown_to_blocks(text), desired_result)
    
    def test_3_normal_blocks(self):
        text = """Line1 is nice
Line2 is very nice
Line3 is cool

Line4
Line5   
Line6

Line8"""
        desired_result = [
            "Line1 is nice\nLine2 is very nice\nLine3 is cool",
            "Line4\nLine5   \nLine6",
            "Line8"
        ]
        self.assertEqual(markdown_to_blocks(text), desired_result)

    def test_empty_string(self):
        text = ""
        desired_result = []

        self.assertEqual(markdown_to_blocks(text), desired_result)

    def test_multiple_lines_between_blocks(self):
        text = "Line1\n\n\nLine2\n\n\nLine3"
        desired_result = ["Line1", "Line2", "Line3"]
        
        self.assertEqual(markdown_to_blocks(text), desired_result)

    def test_with_two_newlines_end(self):
        text = "Line1\n\nLine2\n\nLine3\n\n"
        desired_result = ["Line1", "Line2", "Line3"]
        
        self.assertEqual(markdown_to_blocks(text), desired_result)

    def test_with_trailing_double_newline(self):
        text = "\n\nLine1\n\nLine2\n\nLine3\n\n"
        desired_result = ["Line1", "Line2", "Line3"]
        
        self.assertEqual(markdown_to_blocks(text), desired_result)

    def boot_dev_example(self):
        text = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items"""
        desired_result = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items"
            ]
        self.assertEqual(markdown_to_blocks(text), desired_result)

    def test_with_a_lot_of_newlines(self):
        text = "Line1\n\n\n\n\n\n\n\n\nLine2\n\nLine3\n\n"
        desired_result = ["Line1", "Line2", "Line3"]
        
        self.assertEqual(markdown_to_blocks_solution(text), desired_result)


class TestBlockToBlockType(unittest.TestCase):
    def test_headings(self):
        block = "# This is a Heading"
        block2 = "## This is a Heading"
        block3 = "### This is a Heading"
        block4 = "#### This is a Heading"
        block5 = "##### This is a Heading"
        block6 = "###### This is a Heading"
        desired_result = "heading"

        self.assertEqual(block_to_block_type(block), desired_result)
        self.assertEqual(block_to_block_type(block2), desired_result)
        self.assertEqual(block_to_block_type(block3), desired_result)
        self.assertEqual(block_to_block_type(block4), desired_result)
        self.assertEqual(block_to_block_type(block5), desired_result)
        self.assertEqual(block_to_block_type(block6), desired_result)

    def test_7_heading(self):
        block = "####### This is not a heading"
        undesired_result = "heading"

        self.assertNotEqual(block_to_block_type(block), undesired_result)

    def test_heading_without_space(self):
        block = "####This is not a heading"
        undesired_result = "heading"

        self.assertNotEqual(block_to_block_type(block), undesired_result)

    def test_heading_without_text(self):
        block = "#### "
        undesired_result = "heading"

        self.assertNotEqual(block_to_block_type(block), undesired_result)

    def test_code_blocks(self):
        block = "``` this is some code ```"
        desired_result = "code"

        self.assertEqual(block_to_block_type(block), desired_result)

    def test_code_blocks_multiline(self):
        block = "```\nthis is some code\n```"
        block2 = "```\n\nthis is some code\n\n text\n\nprint('hello world')```"

        desired_result = "code"

        self.assertEqual(block_to_block_type(block), desired_result)
        self.assertEqual(block_to_block_type(block2), desired_result)

    def test_not_code(self):
        block = " ``` bla bla ``"
        block2 = " ``` bla bla ```"
        block3 = "``` bla bla"
        undesired_result = "code"

        self.assertNotEqual(block_to_block_type(block), undesired_result)
        self.assertNotEqual(block_to_block_type(block2), undesired_result)
        self.assertNotEqual(block_to_block_type(block3), undesired_result)
    
    def test_quote_blocks(self):
        block = "> This is a quote"
        block2 = "> This is a quote\n> This is a quote\n> This is a quote"
        block3 = ">This is a quote\n>This is a quote\n>This is a quote"
        desired_result = "quote"

        self.assertEqual(block_to_block_type(block), desired_result)
        self.assertEqual(block_to_block_type(block2), desired_result)
        self.assertEqual(block_to_block_type(block3), desired_result)

    def test_not_quote(self):
        block = " > bla bla"
        block2 = ">bla\nbla\n>bla"
        block3 = ">bla\n>bla\n >blas"
        undesired_result = "quote"

        self.assertNotEqual(block_to_block_type(block), undesired_result)
        self.assertNotEqual(block_to_block_type(block2), undesired_result)
        self.assertNotEqual(block_to_block_type(block3), undesired_result)

    def test_unordered_list_blocks(self):
        block = "- this is a list"
        block2 = "* this is also a list"
        block3 = "- this is a list\n- this is a list"
        block4 = "- this is a list\n- this is a list"
        block5 = "* this is a list\n* this is a list"
        block6 = "- this is a list\n* this is a list"
        desired_result = "unordered_list"

        self.assertEqual(block_to_block_type(block), desired_result)
        self.assertEqual(block_to_block_type(block2), desired_result)
        self.assertEqual(block_to_block_type(block3), desired_result)
        self.assertEqual(block_to_block_type(block4), desired_result)
        self.assertEqual(block_to_block_type(block5), desired_result)
        self.assertEqual(block_to_block_type(block6), desired_result)

    def test_not_unordered_list(self):
        block = " - this is not a list"
        block2 = " * this is not a list"
        block3 = "- this is not a list\n - this is not a list"
        block4 = " "
        block5 = "-this is not a list\n-asdja"
        block6 = "- this is not a list\n-this is not a list"
        undesired_result = "unordered_list"

        self.assertNotEqual(block_to_block_type(block), undesired_result)
        self.assertNotEqual(block_to_block_type(block2), undesired_result)
        self.assertNotEqual(block_to_block_type(block3), undesired_result)
        self.assertNotEqual(block_to_block_type(block4), undesired_result)
        self.assertNotEqual(block_to_block_type(block5), undesired_result)
        self.assertNotEqual(block_to_block_type(block6), undesired_result)

    def test_ordered_list(self):
        block = "1. this is a list"
        block2 = "1. this is also a list\n2. this is a list"
        block3 = "1. this is also a list\n2. this is a list\n3. this is a list"
        desired_result = "ordered_list"

        self.assertEqual(block_to_block_type(block), desired_result)
        self.assertEqual(block_to_block_type(block2), desired_result)
        self.assertEqual(block_to_block_type(block3), desired_result)

    def test_not_ordered_list(self):
        block = "2. this is not a list"
        block2 = "1. this is not a list\n3. this is not a list"
        block3 = "1. this is not a list\n2.this is not a list"
        block4 = " "
        block5 = "1.this is not a list\n2. this is not a list"
        block6 = "1. this is not a list\n- this is not a list"
        undesired_result = "ordered_list"

        self.assertNotEqual(block_to_block_type(block), undesired_result)
        self.assertNotEqual(block_to_block_type(block2), undesired_result)
        self.assertNotEqual(block_to_block_type(block3), undesired_result)
        self.assertNotEqual(block_to_block_type(block4), undesired_result)
        self.assertNotEqual(block_to_block_type(block5), undesired_result)
        self.assertNotEqual(block_to_block_type(block6), undesired_result)
