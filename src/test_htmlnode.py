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

    def test_parent_with_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
    def test_parent_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_with_multiple_children(self):
        child_node = LeafNode("b", "Bold text")
        other_child = LeafNode(None, "Normal text")
        other_node = LeafNode("i", "Italic text")
        parent_node = ParentNode("p", [child_node, other_child, other_node])

        self.assertEqual(
            parent_node.to_html(), 
            "<p><b>Bold text</b>Normal text<i>Italic text</i></p>"
        )
    def test_to_html_with_nested_children_and_props(self):
        inner_child = LeafNode("em", "emphasized", {"class": "highlight"})
        middle_child = ParentNode("span", [inner_child], {"id": "middle"})
        outer_parent = ParentNode("div", [
            LeafNode("p", "First paragraph"),
            middle_child,
            LeafNode("p", "Last paragraph")
        ], {"class": "container"})

        self.assertEqual(
            outer_parent.to_html(),
            '<div class="container"><p>First paragraph</p><span id="middle"><em class="highlight">emphasized</em></span><p>Last paragraph</p></div>'
        )

if __name__ == "__main__":
    unittest.main()