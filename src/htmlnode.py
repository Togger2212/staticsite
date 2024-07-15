

class HTMLNode:
    def __init__(self,tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("not implemented")
    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for key, value in self.props.items():
            props_html += f' {key}="{value}"'
        return props_html
        
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError("A value must be provided for LeafNode.")
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.tag is None:
            return self.value
        if isinstance(self.value, str):
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        else:
            return ValueError("Value needs to be a string")
        
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if not isinstance(children, list) or len(children) == 0:
            raise  ValueError("Children must be provided")
        super().__init__(tag, props)
        self.children = children

    def to_html(self):
        if self.tag is None:
            raise ValueError("tag must be provided")
        if self.children is None:
            raise ValueError("Parent needs Children!")
        parent_string = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            parent_string += child.to_html()
        return parent_string + f"</{self.tag}>"
    


        
        