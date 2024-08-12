import unittest

from textnode import TextNode, text_node_to_html_node, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is text node 1", TextType.TEXT)
        node2 = TextNode("This is text node 2", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_url_none(self):
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertIsNone(node.url, None)

    def test_url_not_none(self):
        node = TextNode("This is a text node", TextType.TEXT, 'localhost')
        self.assertIsNotNone(node.url, None)

    def test_text_to_html_raw(self):
        # Test raw
        node_raw = TextNode('raw text', TextType.TEXT)
        leaf_node_raw = text_node_to_html_node(node_raw)
        self.assertEqual(leaf_node_raw.to_html(), 'raw text')
        self.assertIsNone(leaf_node_raw.tag)

    def test_text_to_html_any_tag(self):
        # Test a tag
        node_code = TextNode('import python', TextType.CODE)
        leaf_node_code = text_node_to_html_node(node_code)
        self.assertEqual(leaf_node_code.to_html(), '<code>import python</code>')
        self.assertIsNotNone(leaf_node_code.tag)

    def test_text_to_html_props(self):
        # test props
        node_image = TextNode('images', TextType.IMAGE, 'localhost')
        leaf_node_image = text_node_to_html_node(node_image)
        expected = '<img src="localhost" alt="images"></img>'
        self.assertEqual(leaf_node_image.to_html(), expected)

    def test_text_to_html_raises(self):
        node = TextNode('Text', 'foo')
        with self.assertRaises(ValueError) as cm:
            text_node_to_html_node(node)
        self.assertEqual('Invalid text_type, got foo', str(cm.exception))


if __name__ == "__main__":
    unittest.main()
