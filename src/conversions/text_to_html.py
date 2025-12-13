from htmlnode import LeafNode
from textnode import TextType
from conversions.split_delimiters import split_node_delimiters, split_nodes_image, split_nodes_link  # noqa F501
import pdb  # noqa F501


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(
                None,
                text_node.text,
                None
            )

        case TextType.BOLD:
            return LeafNode(
                "b",
                text_node.text,
                None
            )

        case TextType.ITALICS:
            return LeafNode(
                "i",
                text_node.text,
                None
            )

        case TextType.CODE:
            return LeafNode(
                "code",
                text_node.text,
                None
            )

        case TextType.LINKS:
            return LeafNode(
                "a",
                text_node.text,
                {"href": text_node.url}
            )

        case TextType.IMAGES:
            return LeafNode(
                "img",
                "",
                {"src": text_node.url, "alt": text_node.text}
            )

        case _:
            raise Exception("Not a valid text node type.")
