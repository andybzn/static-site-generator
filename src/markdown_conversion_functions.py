from src.markdown_block_functions import block_to_block_type, markdown_to_blocks
from src.markdown_inline_functions import text_to_textnodes
from src.nodes_textnode import text_node_to_html_node
from src.nodes_htmlnode import ParentNode


def text_to_children(text):
    """Takes a markdown formatted string, splits it into nodes based on markdown
    formatting, and returns those nodes

    :param text: A string of markdown formatted text
    :type text: str
    :returns: A list of LeafNodes
    :rtype: list(LeafNode)
    """
    return list(map(text_node_to_html_node, text_to_textnodes(text)))


def parse_ordered_list(block):
    """Takes a markdown ordered list block, transforms it into nodes, and returns
    those nodes

    :param block: A string of markdown formatted text
    :type block: str
    :returns: A list of ParentNodes with `li` tags
    :rtype: list(ParentNode)
    """
    return list(
        map(
            lambda x: ParentNode("li", text_to_children(x.split(" ", maxsplit=1)[1])),
            block.split("\n"),
        )
    )


def parse_unordered_list(block):
    """Takes a markdown unordered list block, transforms it into nodes, and
    returns those nodes

    :param block: A string of markdown formatted text
    :type block: str
    :returns: A list of ParentNodes with `li` tags
    :rtype: list(ParentNode)
    """
    return list(
        map(
            lambda item: ParentNode(
                "li", text_to_children(item.removeprefix("- ").removeprefix("* "))
            ),
            block.split("\n"),
        )
    )


def parse_quote(block):
    """Takes a markdown blockquote, transforms it into nodes, and returns those
    nodes

    :param block: A string of markdown formatted text
    :type block: str
    :returns: A list of LeafNodes
    :rtype: list(LeafNode)
    """
    return text_to_children(
        " ".join(list(map(lambda x: x.lstrip("> "), block.split("\n"))))
    )


def parse_code(block):
    """Takes a markdown formatted code block, transforms it into a node, and
    returns that node

    :param block: A string of markdown formatted text
    :type block: str
    :returns: A list containing a single ParentNode with a `code` tag
    :rtype: list(ParentNode)
    """
    return [ParentNode("code", text_to_children(block.strip("```").removeprefix("\n")))]


def parse_headings(block):
    """Takes a markdown heading, transforms it into a node with the appropriate
    heading level, and returns that node

    :param block: A string of markdown formatted text
    :type block: str
    :returns: A single ParentNode with a `h` tag
    :rtype: ParentNode
    """
    return ParentNode(f"h{block.count('#')}", text_to_children(block.lstrip("# ")))


def markdown_to_html_node(markdown):
    """Takes a markdown document, processes it into its component nodes, wraps them
    in a ParentNode with a `div` tag

    :param markdown: A markdown document
    :type markdown: str
    :returns: A single ParentNode with a `div` tag
    :rtype: ParentNode
    """
    markdown_blocks = markdown_to_blocks(markdown)

    nodes = []
    for block in markdown_blocks:
        match block_to_block_type(block):
            case "heading":
                nodes.append(parse_headings(block))
            case "paragraph":
                nodes.append(ParentNode("p", text_to_children(block)))
            case "code":
                nodes.append(ParentNode("pre", parse_code(block)))
            case "ordered_list":
                nodes.append(ParentNode("ol", parse_ordered_list(block)))
            case "unordered_list":
                nodes.append(ParentNode("ul", parse_unordered_list(block)))
            case "quote":
                nodes.append(ParentNode("blockquote", parse_quote(block)))
            case _:
                raise ValueError("invalid block type")

    return ParentNode("div", nodes)
