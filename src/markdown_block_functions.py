import re


def markdown_to_blocks(markdown):
    """Takes a markdown document and returns a list of blocks

    :param markdown: A markdown document
    :type markdown: str
    :returns: A list of markdown blocks
    :rtype: list
    """
    blocks = []
    for block in markdown.split("\n\n"):
        block = block.strip()
        if block != "":
            blocks.append(block)
    return blocks


def block_to_block_type(markdown_block):
    """Takes a markdown block and returns the block type

    :param markdown_block: A block of markdown
    :type markdown_block: block
    :returns: A string containing one of the following types: paragraph, heading, code, quote, unordered_list, ordered list
    :rtype: str
    """

    if re.search(r"^#{1,6}\s", markdown_block):
        return "heading"
    elif re.search(r"^`{3}([\s\S]*)`{3}$", markdown_block, re.MULTILINE):
        return "code"
    elif re.search(r"^(>)\s(.*)$", markdown_block, re.MULTILINE):
        return "quote"
    elif re.search(r"^(-|\*)\s(.*)$", markdown_block, re.MULTILINE):
        return "unordered_list"
    elif re.search(r"^\d{1,3}\.\s(.*)$", markdown_block, re.MULTILINE):
        return "ordered_list"
    else:
        return "paragraph"
