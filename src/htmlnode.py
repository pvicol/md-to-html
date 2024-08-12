class HTMLNode:
    """
    An HTMLNode without a tag will just render as raw text
    An HTMLNode without a value will be assumed to have children
    An HTMLNode without children will be assumed to have a value
    An HTMLNode without props simply won't have any attributes
    """

    def __init__(self,
                 tag: str = None,
                 value: str = None,
                 children: list = None,
                 props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        propped_html = ''
        for k, v in self.props.items():
            propped_html += f' {k}="{v}"'

        # Strip spaces but keep the first white space
        return f' {propped_html.strip()}'

    def __repr__(self) -> str:
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'

    def __qe__(self, other: 'HTMLNode') -> bool:
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props


class LeafNode(HTMLNode):
    def __init__(self, tag: str = None, value: str = None, props: dict = None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):

        # Value is required
        if self.value is None:
            raise ValueError('value is required')

        # Raw text if no tag
        if self.tag is None:
            return self.value

        # Add opening tag
        html_string = f'<{self.tag}'

        # Add props if there are any
        if self.props:
            html_string += f'{self.props_to_html()}'

        # Add value and close tag
        html_string += f'>{self.value}</{self.tag}>'

        # Return HTML string
        return html_string


class ParentNode(HTMLNode):

    def __init__(self, tag: str = None, children: list = None, props: dict = None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        # Tag is required
        if self.tag is None:
            raise ValueError('tag is required')

        # Children are required
        if self.children is None:
            raise ValueError('children are required')

        # Children must be a list
        if not isinstance(self.children, list):
            raise TypeError(f'children must be a list, got {type(self.children).__name__}')

        # HTML String - Open tag
        html_string = f'<{self.tag}'

        # HTML String - Add props
        if self.props:
            html_string += f'{self.props_to_html()}'

        # HTML String - Close tag
        html_string += '>'

        # Loop through children
        for child in self.children:

            # Check if child is LeafNode or ParentNode
            if not isinstance(child, (LeafNode, ParentNode)):
                raise TypeError(f'child must be LeafNode or ParentNode, got {type(child).__name__}')

            # Convert and add to string
            html_string += child.to_html()

        # HTML String - close tag ending
        html_string += f'</{self.tag}>'

        return html_string
