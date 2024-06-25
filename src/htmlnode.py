class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        html = ""
        for prop_key in self.props:
            html += f'{prop_key}="{self.props[prop_key]}" '

        # to remove the trailing whitespace
        return html[:-1]
    
    def __repr__(self):
        return f"Tag: {self.tag} | Value: {self.value} | Children: {self.children} | Props: {self.props}"
    
class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf node has no value")

        if self.tag is None:
            return self.value
        
        if (self.props is None) or (len(self.props) == 0):
            return f'<{self.tag}>{self.value}</{self.tag}>'
        
        return f'<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, children, tag=None, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("HTML tag is not present")
        if (self.children is None) or (len(self.children) == 0):
            raise ValueError("Parent node has no children")
        
        if self.props is None:
            full_html = f'<{self.tag}>'
        else:
            full_html = f'<{self.tag} {self.props_to_html()}>'

        for child_node in self.children:
            child_html = child_node.to_html()
            full_html += child_html
        
        full_html += f"</{self.tag}>"
        return full_html