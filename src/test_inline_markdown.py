import unittest

from textnode import TextType, TextNode

from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_link,
    split_nodes_images,
    text_to_textnodes
)


class TestSplitNode(unittest.TestCase):
    def test_split_nodes_delimiter_raises(self):
        # Test it raises invalid text type
        node = TextNode('text', 'foo')
        with self.assertRaises(ValueError) as cm:
            split_nodes_delimiter([node], 't', 'foo')
        self.assertEqual('Invalid text_type, got foo', str(cm.exception))

    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(expected, new_nodes)

    def test_split_nodes_delimiter_multi(self):
        node = TextNode("This is text with a `code block` word `more`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.TEXT)
        expected = [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word ", TextType.TEXT),
                TextNode('more', TextType.CODE),
                TextNode('', TextType.TEXT)
        ]
        self.assertEqual(expected, new_nodes)

    def test_split_nodes_delimiter_invalid_format(self):
        node = TextNode("This is text with a `code block` word `more", TextType.TEXT)
        with self.assertRaises(ValueError) as cm:
            split_nodes_delimiter([node], '`', TextType.TEXT)

        self.assertEqual(str(cm.exception), 'Invalid markdown, formatted section not close')

    def test_split_nodes_delimiter_invalid_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.TEXT)
        self.assertEqual(new_nodes, [TextNode('', TextType.TEXT)])

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        actual = extract_markdown_images(text)
        self.assertEqual(expected, actual)

    def test_extract_markdown_images_empty(self):
        text = ""
        expected = []
        actual = extract_markdown_images(text)
        self.assertEqual(expected, actual)

    def test_extract_markdown_images_incomplete(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg"
        expected = []
        actual = extract_markdown_images(text)
        self.assertEqual(expected, actual)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        actual = extract_markdown_links(text)
        self.assertEqual(expected, actual)

    def test_extract_markdown_links_empty(self):
        text = ""
        expected = []
        actual = extract_markdown_links(text)
        self.assertEqual(expected, actual)

    def test_extract_markdown_links_incomplete(self):
        text = "This is text with a link [to boot dev(https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev"
        expected = []
        actual = extract_markdown_links(text)
        self.assertEqual(expected, actual)

    def test_split_nodes_links_invalid_type(self):
        with self.assertRaises(TypeError) as cm:
            split_nodes_link(['boo'])

        self.assertEqual(str(cm.exception), 'Invalid node type, got str')

    def test_split_nodes_links(self):
        node = TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                TextType.TEXT,
        )
        actual = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(expected, actual)

    def test_split_nodes_links_none(self):
        node = TextNode(
                "This is text with a no links",
                TextType.TEXT,
        )
        actual = split_nodes_link([node])
        expected = [node]
        self.assertEqual(expected, actual)

    # This may not be needed as the error is never raised regardless of input
    # def test_split_nodes_links_raises(self):
    #     node = TextNode(
    #             "This is text with a link [to boot dev](https://www.boot.dev and ![to youtube](https://www.youtube.com/@bootdotdev)",
    #             TextType.TEXT,
    #     )
    #     with self.assertRaises(ValueError) as cm:
    #         nodes = split_nodes_link([node])
    #         print(nodes)
    #
    #     self.assertEqual(str(cm.exception), 'Invalid markdown, link section not closed')

    def test_split_nodes_images(self):
        node = TextNode(
                "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
                TextType.TEXT,
        )
        actual = split_nodes_images([node])
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(expected, actual)

    def test_text_to_textnodes(self):
        text = 'This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)' # noqa
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        actual = text_to_textnodes(text)

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
