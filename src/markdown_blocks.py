import re


from htmlnode import HTMLNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node


class BlockType:
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'


HTML_TAG_MAPPING = {
        BlockType.PARAGRAPH: {
                'tag': 'p'
        },
        BlockType.HEADING: {
                'tag': 'h'
        },
        BlockType.CODE: {
                'tag': 'code',
                'parent': 'pre'
        },
        BlockType.QUOTE: {
                'tag': 'blockquote'
        },
        BlockType.UNORDERED_LIST: {
                'tag': 'li',
                'parent': 'ul'
        },
        BlockType.ORDERED_LIST: {
                'tag': 'li',
                'parent': 'ol'
        }
}


def markdown_to_blocks(text: str) -> list:
    blocks = []

    split_blocks = text.split('\n\n')

    # Trim spaces
    for block in split_blocks:
        # Skip empty blocks
        if not block:
            continue

        # Add to blocks
        blocks.append(block.strip())

    return blocks


def is_ordered_list_block(text):
    lines = text.splitlines()

    for i, line in enumerate(lines):
        expected_number = i + 1
        pattern = rf'^{expected_number}\. .*$'
        if not re.match(pattern, line):
            return False

    return True


def block_to_block_type(block: str) -> str:

    # Headings start with 1-6 # characters, followed by a space and then the heading text.
    if re.match(r'^(#){1,6} \w.*', block):
        return BlockType.HEADING

    # Code blocks must start with 3 backticks and end with 3 backticks.
    if re.match(r'(^```[\s\S]*```$)', block):
        return BlockType.CODE

    # Every line in a quote block must start with a > character
    if all([line.startswith('>') for line in block.splitlines()]):
        return BlockType.QUOTE

    # Every line in an unordered list block must start with a * or - character, followed by a space.
    if re.match(r'^(?:[*-] .*(?:\n|$))+$', block):
        return BlockType.UNORDERED_LIST

    # Every line in an ordered list block must start with a number followed by a . character and a space.
    # The number must start at 1 and increment by 1 for each line.
    if is_ordered_list_block(block):
        return BlockType.ORDERED_LIST

    # If none of the above conditions are met, the block is a normal paragraph.
    return BlockType.PARAGRAPH


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def process_blockquote(text: str) -> HTMLNode:
    lines = text.splitlines()
    new_lines = []
    for line in lines:
        if not line.startswith('>'):
            raise ValueError('Invalid quote block')
        new_lines.append(line.lstrip('>').strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode(HTML_TAG_MAPPING[BlockType.QUOTE].get('tag'), children=children)


def process_heading(text: str) -> HTMLNode:
    heading_number = re.match(r'^#{1,6} ', text)
    heading_text = text.replace(heading_number.group(), '')
    header_number = len(heading_number.group().strip())
    children = text_to_children(heading_text)
    return ParentNode(f'{HTML_TAG_MAPPING[BlockType.HEADING].get("tag")}{header_number}', children=children)


def process_paragraph(text: str) -> HTMLNode:
    # TODO: Add unit test
    children = text_to_children(text)
    return ParentNode(HTML_TAG_MAPPING[BlockType.PARAGRAPH].get('tag'), children=children)


def process_code(text: str) -> HTMLNode:
    # TODO: Add unit test
    code_lines = text.splitlines()

    code_lines = code_lines[1:-1]
    children = text_to_children('\n'.join(code_lines))
    code_block = ParentNode(HTML_TAG_MAPPING[BlockType.CODE].get('tag'), children=children)
    return ParentNode(HTML_TAG_MAPPING[BlockType.CODE].get('parent'), children=[code_block])


def process_unordered_list(text: str) -> HTMLNode:
    list_items = text.splitlines()
    list_html_nodes = [ParentNode(HTML_TAG_MAPPING[BlockType.UNORDERED_LIST].get('tag'), text_to_children(item[2:])) for item in list_items]
    return ParentNode(HTML_TAG_MAPPING[BlockType.UNORDERED_LIST].get('parent'), children=list_html_nodes)


def process_ordered_list(text: str) -> HTMLNode:
    list_items = text.splitlines()
    list_html_nodes = [ParentNode(HTML_TAG_MAPPING[BlockType.ORDERED_LIST].get('tag'), text_to_children(item[3:])) for item in list_items]
    return ParentNode(HTML_TAG_MAPPING[BlockType.ORDERED_LIST].get('parent'), children=list_html_nodes)


def markdown_to_html_node(markdown: str) -> HTMLNode:
    if not isinstance(markdown, str):
        raise TypeError(f'markdown is not string type, got {type(markdown).__name__}')

    # Split markdown into blocks
    raw_blocks = markdown_to_blocks(markdown)
    html_block_nodes = []

    # Get type of each block
    for block in raw_blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.QUOTE:
                blockquote = process_blockquote(block)
                html_block_nodes.append(blockquote)

            case BlockType.HEADING:
                heading = process_heading(block)
                html_block_nodes.append(heading)

            case BlockType.CODE:
                code = process_code(block)
                html_block_nodes.append(code)

            case BlockType.UNORDERED_LIST:
                ul = process_unordered_list(block)
                html_block_nodes.append(ul)

            case BlockType.ORDERED_LIST:
                ol = process_ordered_list(block)
                html_block_nodes.append(ol)

            # All other types will be processed as paragraphs
            case _:
                paragraph = process_paragraph(block)
                html_block_nodes.append(paragraph)

    return ParentNode('div', children=html_block_nodes)
