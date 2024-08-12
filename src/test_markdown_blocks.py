import unittest

from markdown_blocks import (
    BlockType,
    markdown_to_blocks,
    is_ordered_list_block,
    block_to_block_type,
    process_blockquote,
    process_heading,
    process_unordered_list,
    process_ordered_list
)
from htmlnode import ParentNode, LeafNode


class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md_text = '''# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item'''

        expected = [
                '# This is a heading',
                'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
                '''* This is the first list item in a list block
* This is a list item
* This is another list item'''
        ]

        actual = markdown_to_blocks(md_text)
        self.assertEqual(expected, actual)

    def test_markdown_to_blocks_extra(self):
        # Text below has extra new lines and extra white spaces
        md_text = '''# This is a heading




This is a paragraph of text. It  has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item 
* This is another list item''' # noqa

        expected = [
                    '# This is a heading',
                    'This is a paragraph of text. It  has some **bold** and *italic* words inside of it.',
                    '''* This is the first list item in a list block
* This is a list item 
* This is another list item''' # noqa
            ]

        actual = markdown_to_blocks(md_text)
        self.assertEqual(expected, actual)

    def test_is_ordered_list_block_true(self):
        num_list = """1. First item
2. Second item
3. Third item
4. Fourth item
"""

        self.assertTrue(is_ordered_list_block(num_list))

    def test_is_ordered_list_block_false(self):
        num_list = """1. First item
2. Second item
420. Third item
69. Fourth item
"""

        self.assertFalse(is_ordered_list_block(num_list))

    def test_block_to_block_type_heading(self):
        text = '## Heading 2'
        self.assertEqual(BlockType.HEADING, block_to_block_type(text))

    def test_block_to_block_type_not_heading(self):
        text = '##Heading 2'
        self.assertNotEqual(BlockType.HEADING, block_to_block_type(text))

    def test_block_to_block_type_code(self):
        text = '''```this is a code
        block
        because import python
```
'''
        self.assertEqual(BlockType.CODE, block_to_block_type(text))

    def test_block_to_block_type_not_code(self):
        text = '''```this is a code
        block
        because import python
'''
        self.assertNotEqual(BlockType.CODE, block_to_block_type(text))

    def test_block_to_block_type_quote(self):
        text = '''>Some
> Quote
'''
        self.assertEqual(BlockType.QUOTE, block_to_block_type(text))

    def test_block_to_block_type_not_quote(self):
        text = '''>Some
Not Quote
'''
        self.assertNotEqual(BlockType.QUOTE, block_to_block_type(text))

    def test_block_to_block_type_ul(self):
        text = '''* Item 1
- Item 2
'''
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(text))

    def test_block_to_block_type_not_ul(self):
        text = '''* Item 1
2. Item 2
'''
        self.assertNotEqual(BlockType.UNORDERED_LIST, block_to_block_type(text))

    def test_block_to_block_type_ol(self):
        text = '''1. Item 1
2. Item 2
'''
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(text))

    def test_block_to_block_type_not_ol(self):
        text = '''1. Item 1
> Item 2
'''
        self.assertNotEqual(BlockType.ORDERED_LIST, block_to_block_type(text))

    def test_block_to_block_type_paragraph(self):
        text = '''An good ole paragraph
'''
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(text))

    def test_block_to_block_type_paragraph_all(self):
        text = '''```Code block but```
1. With
2. A
- List
'''
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(text))

    def test_process_blockquote(self):
        text = """> This is a
>quote block"""
        expected = ParentNode('blockquote', [LeafNode(None, """This is a
quote block""")])
        actual = process_blockquote(text)
        self.assertEqual(expected.tag, actual.tag)
        self.assertEqual(expected.value, actual.value)

    def test_process_heading(self):
        text = '### Heading3'
        expected = ParentNode('h3', [LeafNode(None, 'Heading3')])
        actual = process_heading(text)
        self.assertEqual(expected.tag, actual.tag)
        self.assertEqual([item.value for item in expected.children], [item.value for item in actual.children])

    def test_process_ordered_list(self):
        text = """1. Ordered
2. List"""
        expected = ParentNode('ol', children=[
                ParentNode('li', [LeafNode(None, 'Ordered')]),
                ParentNode('li', [LeafNode(None, 'List')])
        ])
        actual = process_ordered_list(text)
        # Test tag is ol
        self.assertEqual(expected.tag, actual.tag)
        # Test all children are 'li'
        self.assertTrue(all(['li' == item.tag for item in actual.children]))
        # Test children values match
        self.assertEqual([item.value for item in expected.children], [item.value for item in actual.children])

    def test_process_unordered_list(self):
        text = """* Unordered
- List"""
        expected = ParentNode('ul', children=[
                ParentNode('li', [LeafNode(None, 'Unordered')]),
                ParentNode('li', [LeafNode(None, 'List')])
        ])
        actual = process_unordered_list(text)
        # Test tag is ul
        self.assertEqual(expected.tag, actual.tag)
        # Test all children are 'li'
        self.assertTrue(all(['li' == item.tag for item in actual.children]))
        # Test children values match
        self.assertEqual([item.value for item in expected.children], [item.value for item in actual.children])


if __name__ == '__main__':
    unittest.main()
