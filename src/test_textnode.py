import unittest
import pdb  # noqa F501
from textnode import TextNode, TextType
from conversions.split_delimiters import text_to_textnodes


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode(
            "This is a text node",
            TextType.BOLD
        )
        node2 = TextNode(
            "This is a text node",
            TextType.BOLD
        )
        self.assertEqual(node, node2)

    def test_diff_type(self):
        node = TextNode(
            "This is a text node",
            TextType.BOLD
        )
        node2 = TextNode(
            "This is a text node",
            TextType.ITALICS
        )
        self.assertNotEqual(node, node2)

    def test_link(self):
        node = TextNode(
            "This node should have a link",
            TextType.LINKS,
            "https://boot.dev"
        )
        self.assertEqual("https://boot.dev", node.url)

    def no_link_test(self):
        node = TextNode(
            "This node should not have a link",
            TextType.CODE
        )
        self.assertEqual(None, node.url)


class TestText_to_Node(unittest.TestCase):
    def test_text_to_textnode(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"  # noqa E501
        node = TextNode(text, TextType.TEXT)
        new_nodes = text_to_textnodes(node)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALICS),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image",
                TextType.IMAGES,
                "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode(
                "link",
                TextType.LINKS,
                "https://boot.dev"
            ),
        ]
        self.assertEqual(new_nodes, expected_nodes)
