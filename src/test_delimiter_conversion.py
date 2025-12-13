import unittest
from textnode import TextNode, TextType
from conversions.split_delimiters import split_node_delimiters, split_nodes_image, split_nodes_link  # noqa F501


class TestTextSplits(unittest.TestCase):
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

    def test_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",  # noqa E501
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected_nodes = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode(
                "image",
                TextType.IMAGES,
                "https://i.imgur.com/zjjcJKZ.png"
            ),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image",
                TextType.IMAGES,
                "https://i.imgur.com/3elNhQu.png"
            ),
        ]
        self.assertListEqual(expected_nodes, new_nodes)

        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) This node started with an image.",  # noqa E501
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected_nodes = [
            TextNode(
                "image",
                TextType.IMAGES,
                "https://i.imgur.com/zjjcJKZ.png"
            ),
            TextNode(" This node started with an image.", TextType.TEXT),
        ]
        self.assertListEqual(expected_nodes, new_nodes)

        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)This node has two images back-to-back.",  # noqa E501
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected_nodes = [
            TextNode(
                "image",
                TextType.IMAGES,
                "https://i.imgur.com/zjjcJKZ.png"
            ),
            TextNode(
                "second image",
                TextType.IMAGES,
                "https://i.imgur.com/3elNhQu.png"
            ),
            TextNode("This node has two images back-to-back.", TextType.TEXT),
        ]
        self.assertListEqual(expected_nodes, new_nodes)

    def test_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",  # noqa E501
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode(
                "link",
                TextType.LINKS,
                "https://i.imgur.com/zjjcJKZ.png"
            ),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second link",
                TextType.LINKS,
                "https://i.imgur.com/3elNhQu.png"
            ),
        ]
        self.assertListEqual(expected_nodes, new_nodes)
