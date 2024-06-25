import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_format_1(self):
        node = HTMLNode("h1", "Title", props={"href": "https://www.google.com", "target": "_blank"})
        desired_result = 'href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), desired_result)
    
    def test_props_to_html_empty(self):
        node = HTMLNode("<h1>", "Title")
        self.assertEqual(node.props_to_html(), "")

class TestLeafNode(unittest.TestCase):
    def test_all_props_present_to_html(self):
        leaf_node = LeafNode(value="This is a paragraph!", tag="p", props={"style": "colorRed"})
        desired_html = '<p style="colorRed">This is a paragraph!</p>'
        self.assertEqual(leaf_node.to_html(), desired_html)
        
    def test_no_tag_to_html(self):
        leaf_node = LeafNode(value="This is a paragraph!", props={"style": "colorRed"})
        desired_html = 'This is a paragraph!'
        self.assertEqual(leaf_node.to_html(), desired_html)
    
    def test_none_value_to_html(self):
        leaf_node = LeafNode(props={"style": "colorRed"}, tag="p", value=None)

        with self.assertRaises(ValueError) as context: 
            leaf_node.to_html()
        self.assertEqual(str(context.exception), "Leaf node has no value")

    def test_empty_value_to_html(self):
        leaf_node = LeafNode(props={"style": "colorRed"}, tag="p", value="")
        desired_html = '<p style="colorRed"></p>'
        self.assertEqual(leaf_node.to_html(), desired_html)

    def test_no_props_to_html(self):
        leaf_node = LeafNode(value="This is a paragraph!", tag="h1")
        desired_html = '<h1>This is a paragraph!</h1>'
        self.assertEqual(leaf_node.to_html(), desired_html)

    def test_empty_props_to_html(self):
        leaf_node = LeafNode(value="This is a paragraph!", tag="h1", props={})
        desired_html = '<h1>This is a paragraph!</h1>'
        self.assertEqual(leaf_node.to_html(), desired_html)

class TestParentNode(unittest.TestCase):
    
    def test_root_with_two_leafs(self):
        leaf_node_1 = LeafNode(value="This is a paragraph!", tag="p", props={"style": "colorRed"})
        leaf_node_2 = LeafNode(value="This is another paragraph!", tag="h2")
        root_node = ParentNode(tag="div", children=[leaf_node_2, leaf_node_1], props={"id":"parentNode"})
        desired_html = '<div id="parentNode"><h2>This is another paragraph!</h2><p style="colorRed">This is a paragraph!</p></div>'
        self.assertEqual(root_node.to_html(), desired_html)

    def test_root_with_one_parent_with_two_child(self):
        leaf_node_1 = LeafNode(value="This is a paragraph!", tag="p", props={"style": "colorRed"})
        leaf_node_2 = LeafNode(value="This is another paragraph!", tag="h2")
        parent_node = ParentNode(tag="div", children=[leaf_node_2, leaf_node_1], props={"id":"parentNode"})
        root_node = ParentNode(tag="div", children=[parent_node], props={"id":"rootNode"})
        desired_html = '<div id="rootNode"><div id="parentNode"><h2>This is another paragraph!</h2><p style="colorRed">This is a paragraph!</p></div></div>'
        self.assertEqual(root_node.to_html(), desired_html)

    def test_root_with_two_parents_one_leaf(self):
        leaf_node_1 = LeafNode(value="This is a paragraph!", tag="p", props={"style": "colorRed"})
        leaf_node_2 = LeafNode(value="This is another paragraph!", tag="h2")
        parent_node = ParentNode(tag="div", children=[leaf_node_2, leaf_node_1], props={"id":"parentNode"})
        parent_node_2 = ParentNode(tag="head", children=[parent_node])
        root_node = ParentNode(tag="div", children=[parent_node, leaf_node_1, parent_node_2], props={"id":"rootNode"})
        desired_html = '<div id="rootNode"><div id="parentNode"><h2>This is another paragraph!</h2><p style="colorRed">This is a paragraph!</p></div>' \
                       '<p style="colorRed">This is a paragraph!</p>' \
                       '<head><div id="parentNode"><h2>This is another paragraph!</h2><p style="colorRed">This is a paragraph!</p></div></head></div>'
        self.maxDiff = None
        self.assertEqual(root_node.to_html(), desired_html)


if __name__ == "__main__":
    unittest.main()