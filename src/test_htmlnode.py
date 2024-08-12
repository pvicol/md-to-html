import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_html_props(self):
        node = HTMLNode("a", "localhost", props={'href': 'localhost', 'target': '_blank'})
        expected_value = ' href="localhost" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_value)

    def test_html_raises_not_implemented_error(self):
        node = HTMLNode("a", "localhost", props={'href': 'localhost', 'target': '_blank'})
        self.assertRaises(NotImplementedError, node.to_html)

    def test_html_none(self):
        node = HTMLNode()
        attributes = ['tag', 'value', 'children', 'props']
        for attr in attributes:
            self.assertIsNone(getattr(node, attr))

    def test_leaf_props(self):
        node = LeafNode("a", "localhost", props={'href': 'localhost', 'target': '_blank'})
        expected_value = ' href="localhost" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_value)

    def test_leaf_to_html(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected_value = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), expected_value)

    def test_leaf_raise_value_error(self):
        node = LeafNode()
        self.assertRaises(ValueError, node.to_html)

    def test_leaf_raw_value(self):
        node = LeafNode(value='Some Value')
        self.assertEqual(node.to_html(), 'Some Value')

    def test_leaf_no_props(self):
        node = LeafNode('p', 'some value')
        expected_output = '<p>some value</p>'
        self.assertEqual(node.to_html(), expected_output)

    def test_parent_no_tag(self):
        node = ParentNode()
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        self.assertEqual(str(cm.exception), 'tag is required')

    def test_parent_no_children(self):
        node = ParentNode('a')
        with self.assertRaises(ValueError) as cm:
            node.to_html()
        self.assertEqual(str(cm.exception), 'children are required')

    def test_parent_children_is_list(self):
        node = ParentNode('a', children='Something else') # noqa - test children not being a list
        with self.assertRaises(TypeError) as cm:
            node.to_html()
        self.assertEqual(str(cm.exception), 'children must be a list, got str')

    def test_parent_child_is_not_leafnode(self):
        node = ParentNode('ul', children=['test'])
        with self.assertRaises(TypeError) as cm:
            node.to_html()
        self.assertEqual(str(cm.exception), 'child must be LeafNode or ParentNode, got str')

    def test_parent_html_string(self):
        node = ParentNode(
                'ul',
                [
                        LeafNode('li', 'item 1'),
                        LeafNode('li', 'item 2'),
                        ParentNode('ol', [
                                LeafNode('li', 'item 3'),
                                LeafNode('li', 'item 4')
                        ])
                ]
        )
        expected_value = '<ul><li>item 1</li><li>item 2</li><ol><li>item 3</li><li>item 4</li></ol></ul>'
        self.assertEqual(node.to_html(), expected_value)

        # Test case from example
        node = ParentNode(
                "p",
                [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                ],
        )

        expected_value = '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        self.assertEqual(node.to_html(), expected_value)


if __name__ == '__main__':
    unittest.main()
