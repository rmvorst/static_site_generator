import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_diff_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALICS)
        self.assertNotEqual(node, node2)

    def test_link(self):
        node = TextNode("This node should have a link", TextType.LINKS, "https://boot.dev")
        self.assertEqual("https://boot.dev", node.url)

    def no_link_test(self):
        node = TextNode("This node should not have a link", TextType.CODE)
        self.assertEqual(None, node.url)



if __name__ == "__main__":
    unittest.main()