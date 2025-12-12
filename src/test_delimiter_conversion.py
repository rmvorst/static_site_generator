import unittest
from textnode import TextNode, TextType
from conversions.split_delimiters import split_node_delimiters


class TestDelimiterSplits(unittest.TestCase):
    def test_code(self):
        # Standard case
        node = TextNode(
            "This is text with a `code block` word",
            TextType.TEXT
        )
        new_nodes = split_node_delimiters([node], "`", TextType.CODE)
        expected_new_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_new_nodes)

        # Multiple delimitered segments
        node = TextNode(
            "This `is text `with two `code block` segments",
            TextType.TEXT
        )
        new_nodes = split_node_delimiters([node], "`", TextType.CODE)
        expected_new_nodes = [
            TextNode("This ", TextType.TEXT),
            TextNode("is text ", TextType.CODE),
            TextNode("with two ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" segments", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_new_nodes)

        # Already a code block test
        node = TextNode(
            "This is already a code block node",
            TextType.CODE
        )
        new_nodes = split_node_delimiters([node], "`", TextType.CODE)
        self.assertEqual([node], new_nodes)

        # Broken delimiter
        node = TextNode(
            "This has a broken `code block delimiter",
            TextType.TEXT
        )
        with self.assertRaises(Exception) as cm:
            split_node_delimiters([node], "`", TextType.CODE)
        self.assertEqual(str(cm.exception), "No closing delimiter found.")

    def test_bold(self):
        # Standard case
        node = TextNode(
            "This is text with a **bold** word",
            TextType.TEXT
        )
        new_nodes = split_node_delimiters([node], "**", TextType.BOLD)
        expected_new_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_new_nodes)

        # Strange case of an extra * for the bold delimiter
        node = TextNode(
            "This is multiple ***bold delimiter** questions.",
            TextType.TEXT
        )
        new_nodes = split_node_delimiters([node], "**", TextType.BOLD)
        expected_new_nodes = [
            TextNode("This is multiple ", TextType.TEXT),
            TextNode("*bold delimiter", TextType.BOLD),
            TextNode(" questions.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_new_nodes)

        # Multiple input node case
        node = [
            TextNode("This has **3** nodes.", TextType.TEXT),
            TextNode("This is the **second** bold node", TextType.TEXT),
            TextNode("This is the third already bold node", TextType.BOLD)
        ]
        new_nodes = split_node_delimiters(node, "**", TextType.BOLD)
        expected_new_nodes = [
            TextNode("This has ", TextType.TEXT),
            TextNode("3", TextType.BOLD),
            TextNode(" nodes.", TextType.TEXT),
            TextNode("This is the ", TextType.TEXT),
            TextNode("second", TextType.BOLD),
            TextNode(" bold node", TextType.TEXT),
            TextNode("This is the third already bold node", TextType.BOLD)
        ]
        self.assertEqual(new_nodes, expected_new_nodes)

    def test_italics(self):
        # Standard case
        node = TextNode(
            "This is text with an _italics_ word",
            TextType.TEXT
        )
        new_nodes = split_node_delimiters([node], "_", TextType.ITALICS)
        expected_new_nodes = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italics", TextType.ITALICS),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_new_nodes)

        # Strange case of an extra _ for the italics delimiter
        node = TextNode(
            "This is multiple __italics delimiter__ question.",
            TextType.TEXT
        )
        new_nodes = split_node_delimiters([node], "_", TextType.ITALICS)
        expected_new_nodes = [
            TextNode("This is multiple ", TextType.TEXT),
            TextNode("", TextType.ITALICS),
            TextNode("italics delimiter", TextType.TEXT),
            TextNode("", TextType.ITALICS),
            TextNode(" question.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_new_nodes)

        # Broken delimiter with multiple nodes
        node = [
            TextNode("This has _3_ nodes.", TextType.TEXT),
            TextNode("This is the second_ bold node", TextType.TEXT),
            TextNode("This is the third italics node", TextType.ITALICS)
        ]
        with self.assertRaises(Exception) as cm:
            split_node_delimiters(node, "_", TextType.CODE)
        self.assertEqual(str(cm.exception), "No closing delimiter found.")
