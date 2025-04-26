import unittest

from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()