import re
from src.nodes_textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes_to_return = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes_to_return.append(node)
            continue

        node_content = node.text.split(delimiter)
        if len(node_content) % 2 == 0:
            raise ValueError(f"Invalid Markdown: no closing delimiter '{delimiter}'")
        new_nodes = []
        for i in range(len(node_content)):
            # cater for blank splits
            if node_content[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(node_content[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(node_content[i], text_type))
        nodes_to_return.extend(new_nodes)

    return nodes_to_return


def extract_markdown_images(text):
    """Takes a line of text and returns the content of any image tags

    :param text:The line of text to parse
    :type text: str
    :returns: A list of tuples containing the alt text and image url: (alt, url)
    :rtype: list
    """
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    """Takes a line of text and returns the content of any link tags

    :param text: The line of text to parse
    :type text: str
    :returns: A list of tuples containing the anchor text and link url: (anchor, url)
    :rtype: list
    """
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes):
    """Takes a list of TextNodes, splits them on an image, and returns the new nodes (wraps split_media_nodes)

    :param old_nodes: A list of TextNodes
    :type old_nodes: list
    :returns: A list of TextNodes
    :rtype: list
    """
    return split_media_nodes(old_nodes, "image")


def split_nodes_link(old_nodes):
    """Takes a list of TextNodes, splits them on a link, and returns the new nodes (wraps split_media_nodes)

    :param old_nodes: A list of TextNodes
    :type old_nodes: list
    :returns: A list of TextNodes
    :rtype: list
    """
    return split_media_nodes(old_nodes, "link")


def split_media_nodes(nodes_to_split, split_type):
    """Takes a list of TextNodes, splits them on either an image or a link, and returns the new nodes

    :param nodes_to_split: A list of TextNodes
    :type nodes_to_split: list
    :param split_type: The type of split ("image" or "link")
    :type split_type: str
    :returns: A list of TextNodes
    :rtype: list
    """

    if split_type not in ("image", "link"):
        raise ValueError(f"Invalid split_type: {split_type}")

    split_type_char = {"image": "!", "link": ""}
    parser = {"image": extract_markdown_images, "link": extract_markdown_links}
    text_type = {"image": TextType.IMAGE, "link": TextType.LINK}

    nodes_to_return = []
    for node in nodes_to_split:
        if node.text_type != TextType.TEXT:
            nodes_to_return.append(node)
            continue

        media_urls = parser[split_type](node.text)
        if len(media_urls) == 0:
            nodes_to_return.append(node)
            continue

        node_content = node.text
        for a, b in media_urls:
            splits = node_content.split(f"{split_type_char[split_type]}[{a}]({b})", 1)
            if len(splits) != 2:
                raise ValueError("Invalid markdown, section not closed")

            if splits[0] != "":
                nodes_to_return.append(TextNode(splits[0], TextType.TEXT))
            nodes_to_return.append(TextNode(a, text_type[split_type], b))

            node_content = splits[1]

        if node_content != "":
            nodes_to_return.append(TextNode(node_content, TextType.TEXT))

    return nodes_to_return


def text_to_textnodes(text):
    """Takes a string, splits them by formatting, and returns a list of TextNodes

    :param text: A text string
    :type text: str
    :returns: A list of TextNodes
    :rtype: list
    """
    nodes_to_return = [TextNode(text, TextType.TEXT)]
    nodes_to_return = split_nodes_delimiter(nodes_to_return, "**", TextType.BOLD)
    nodes_to_return = split_nodes_delimiter(nodes_to_return, "*", TextType.ITALIC)
    nodes_to_return = split_nodes_delimiter(nodes_to_return, "`", TextType.CODE)
    nodes_to_return = split_nodes_image(nodes_to_return)
    nodes_to_return = split_nodes_link(nodes_to_return)
    return nodes_to_return
