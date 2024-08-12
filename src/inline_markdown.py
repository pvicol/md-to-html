import re

from textnode import TextType, TextNode

DELIMITER_MAPPING = {
        '`': TextType.CODE,
        '*': TextType.ITALIC,
        '**': TextType.BOLD
}


def split_nodes_delimiter(old_nodes: [TextNode], delimiter: str, text_type: str) -> list:
    if text_type not in [v for k, v in TextType.__dict__.items() if not k.startswith('__')]:
        raise ValueError(f'Invalid text_type, got {text_type}')

    new_nodes = []
    for node in old_nodes:

        # We only split text nodes, all other types can be ignored
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        splits = node.text.split(delimiter)
        if len(splits) % 2 == 0:
            raise ValueError('Invalid markdown, formatted section not close')

        for index, part in enumerate(splits):
            if index % 2 == 0:
                found_node = TextNode(part, TextType.TEXT)
            else:
                found_node = TextNode(part, DELIMITER_MAPPING[delimiter])
            new_nodes.append(found_node)
    return new_nodes


def split_nodes_link(old_nodes: [TextNode]) -> [TextNode]:
    new_nodes = []
    for node in old_nodes:

        # Raise error if node is not TextNode
        if not isinstance(node, TextNode):
            raise TypeError(f'Invalid node type, got {type(node).__name__}')

        # If the Node text type is not (raw) text, we can add and continue
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # Store node text into variable to manipulate
        original_text = node.text

        # Get the links from the text
        found_links = extract_markdown_links(original_text)

        # If links are not found, simply append to the list and move on
        if not found_links:
            new_nodes.append(node)
            continue

        for link in found_links:
            sections = original_text.split(f'[{link[0]}]({link[1]})', 1)

            # We expect to always have 2 section - before and after the link, even if empty
            # This section might not be useful as this error is not raised regardless of input
            if len(sections) != 2:
                raise ValueError('Invalid markdown, link section not closed')

            # If first section is not empty/none, append to new nodes
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            # Append the Link to nodes
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))

            # We append the remaining section to the original text to be processed by the next iteration
            original_text = sections[1]

        # Add remaining text as node after all links were extracted
        if original_text:
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes


def split_nodes_images(old_nodes: [TextNode]) -> [TextNode]:
    new_nodes = []
    for node in old_nodes:

        # Raise error if node is not TextNode
        if not isinstance(node, TextNode):
            raise TypeError(f'Invalid node type, got {type(node).__name__}')

        # If the Node text type is not (raw) text, we can add and continue
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # Store node text into variable to manipulate
        original_text = node.text

        # Get the images from the text
        images = extract_markdown_images(original_text)

        # If images are not found, simply append to the list and move on
        if not images:
            new_nodes.append(node)
            continue

        for image in images:
            sections = original_text.split(f'![{image[0]}]({image[1]})', 1)

            # We expect to always have 2 section - before and after the image, even if empty
            # This section might not be useful as this error is not raised regardless of input
            if len(sections) != 2:
                raise ValueError('Invalid markdown, image section not closed')

            # If first section is not empty/none, append to new nodes
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            # Append the image to nodes
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))

            # We append the remaining section to the original text to be processed by the next iteration
            original_text = sections[1]

        # Add remaining text as node after all images were extracted
        if original_text:
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes


def extract_markdown_images(text: str) -> [tuple]:
    find_all_pattern = r'!\[(.*?)\]\((.*?)\)'

    return re.findall(find_all_pattern, text)


def extract_markdown_links(text: str) -> [tuple]:
    find_all_pattern = r'(?<!!)\[(.*?)\]\((.*?)\)'

    return re.findall(find_all_pattern, text)


def text_to_textnodes(text: str) -> [TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]

    # Extract bold text
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)

    # Extract italic
    nodes = split_nodes_delimiter(nodes, '*', TextType.ITALIC)

    # Extract code
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)

    # Extract images
    nodes = split_nodes_images(nodes)

    # Extract links
    nodes = split_nodes_link(nodes)

    return nodes
