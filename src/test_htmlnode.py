import unittest

from htmlnode import HTMLNode, ParentNode, LeafNode, text_node_to_html_node
from textnode import TextNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p","para",None, {"href": "http"})
        tnode = TextNode("hello", "bold")
        nodet = LeafNode("b", "hello")
        node2 = HTMLNode("p","para",None, {"href": "http"})
        node3 = HTMLNode("a", "pap",None, {"fert": "gert"})
        node4 = HTMLNode("g", "bold",[node, node3, node2], {"shi":"bent"})
        node5 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        print(node5.to_html())
        
        
        
        

     


if __name__ == "__main__":
    unittest.main()