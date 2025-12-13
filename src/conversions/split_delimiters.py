import re
import pdb  # noqa F401
from textnode import TextType, TextNode
from conversions.extract_text import extract_markdown_images, extract_markdown_links  # noqa E501


def split_node_delimiters(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        segments = node.text.split(delimiter)
        if len(segments) % 2 == 0:
            raise Exception("No closing delimiter found.")

        counter = 1
        for segment in segments:
            if counter % 2 == 0:
                new_nodes.extend([TextNode(segment, text_type)])
            else:
                new_nodes.extend([TextNode(segment, TextType.TEXT)])
            counter += 1
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    node_texts = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        node_texts.extend(extract_markdown_images(node.text))
        if len(node_texts) == 0:
            raise Exception("Error with image node infomation")

    re_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    segments = re.split(re_pattern, node.text)
    i = 0
    j = 0
    while i < len(segments):
        if segments[i] == "":
            i += 1
            continue
        if segments[i] == node_texts[j][0]:
            new_nodes.extend([TextNode(
                    node_texts[j][0],
                    TextType.IMAGES,
                    node_texts[j][1])
                ]
            )
            i += 1
            if j < len(node_texts)-1:
                j += 1
        else:
            new_nodes.extend([TextNode(segments[i], TextType.TEXT)])
        i += 1
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    node_texts = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        node_texts = extract_markdown_links(node.text)

        if len(node_texts) == 0:
            raise Exception("Error with image node infomation")

    re_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    segments = re.split(re_pattern, node.text)
    i = 0
    j = 0
    while i < len(segments):
        if segments[i] == "":
            i += 1
            continue
        if segments[i] == node_texts[j][0]:
            new_nodes.extend([TextNode(
                    node_texts[j][0],
                    TextType.LINKS,
                    node_texts[j][1])
                ]
            )
            i += 1
            if j < len(node_texts)-1:
                j += 1
        else:
            new_nodes.extend([TextNode(segments[i], TextType.TEXT)])
        i += 1
    return new_nodes
