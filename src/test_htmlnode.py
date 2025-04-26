import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_empty(self):
        node = HTMLNode(props=None)
        result = node.props_to_html()
        self.assertEqual("", result)
    
    def test_multi(self):
        node = HTMLNode(props={"href": "url", "target": "_blank"})
        result = node.props_to_html()
        expected = ' href="url" target="_blank"'
        self.assertEqual(result, expected)
    
    def test_to_html(self):
        with self.assertRaises(NotImplementedError):
            node = HTMLNode()
            node.to_html()

    def test_value_and_children_repr(self):
        child = HTMLNode(value="child text")
        node = HTMLNode(value="parent text", children=child)
        rep = repr(node)
        self.assertIn("parent text", rep)
        self.assertIn("child text", rep)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click Link", {"href": "https://www.dogs.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.dogs.com">Click Link</a>')

    def test_leaf_tag_none(self):
        node = LeafNode(None, "Raw Text")
        self.assertEqual(node.to_html(), "Raw Text")

    def test_leaf_value_none(self):
        with self.assertRaises(ValueError):
            node = LeafNode("p", None)
            node.to_html()

if __name__ == "__main__":
    unittest.main()