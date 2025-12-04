import unittest
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from conversions.text_to_html import text_node_to_html_node


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        props = {"href": "https://www.google.com", "target": "Jack"}

        node = HTMLNode("a", "Testing equivalence", None, props)
        node2 = HTMLNode("a", "Testing equivalence", None, props)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        props = {"href": "https://www.google.com", "target": "Jack"}
        node_child = HTMLNode("p", "Testing equivalence", None, props)

        node = HTMLNode("a", "Testing non-equivalence", None, props)
        node2 = HTMLNode("a", "Testing non-equivalence", [node_child], props)
        self.assertNotEqual(node, node2)

    def test_empty(self):
        node = HTMLNode()
        node2 = HTMLNode(None, None, None, None)
        self.assertEqual(node, node2)


class TestLeafNode(unittest.TestCase):
    def test_text(self):
        leaf_node = LeafNode(
            "p",
            "Plain text paragraph - no links."
        )
        self.assertEqual(
            leaf_node.to_html(),
            "<p>Plain text paragraph - no links.</p>"
        )

    def test_link(self):
        leaf_node = LeafNode(
            "a",
            "Click me!",
            {"href": "https://www.google.com"}
        )
        self.assertEqual(
            leaf_node.to_html(),
            '<a href="https://www.google.com">Click me!</a>'
        )

    def test_no_value(self):
        with self.assertRaises(ValueError) as cm:
            LeafNode("p", None, {"href": "https://www.google.com"}).to_html()
        self.assertEqual(
            str(cm.exception),
            "All leaf nodes must have a value"
        )

    def test_raw_text(self):
        leaf_node = LeafNode(
            None,
            "Plain text paragraph - no links.",
            {"href": "https://www.google.com"}
        )
        self.assertEqual(
            leaf_node.to_html(),
            "Plain text paragraph - no links."
        )


class TestParentNode(unittest.TestCase):
    def test_parent_child(self):
        leaf_node = LeafNode(
            "p",
            "Plain text paragraph - no links."
        )
        parent_node = ParentNode(
            "h1",
            [leaf_node]
        )
        self.assertEqual(
            parent_node.to_html(),
            "<h1><p>Plain text paragraph - no links.</p></h1>"
        )

    def test_parent_mid_child(self):
        props = {"href": "https://www.google.com", "target": "Jack"}
        leaf_node1 = LeafNode(
            "p",
            "Plain text"
        )
        leaf_node2 = LeafNode(
            "a",
            "Click Me!",
            props
        )
        leaf_node3 = LeafNode(
            "p",
            "Plain text"
        )
        leaf_node4 = LeafNode(
            "a",
            "Test Node 4"
        )
        leaf_node5 = LeafNode(
            "span",
            "test"
        )
        nested_parent = ParentNode(
            "div",
            [leaf_node3, leaf_node4, leaf_node5],
        )
        mid_node = ParentNode(
            "p",
            [leaf_node1, nested_parent, leaf_node2]
        )
        parent_node = ParentNode(
            "h1",
            [mid_node]
        )
        expected = (
            '<h1><p><p>Plain text</p><div><p>Plain text</p><a>Test Node 4</a>'
            '<span>test</span></div><a href="https://www.google.com" '
            'target="Jack">Click Me!</a></p></h1>'
        )

        self.assertEqual(
            parent_node.to_html(),
            expected
        )

    def test_to_html_with_children(self):
        child_node = LeafNode(
            "span",
            "child"
        )
        parent_node = ParentNode(
            "div",
            [child_node]
        )
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child</span></div>"
        )

    def test_children_order(self):
        child1 = LeafNode(
            "b",
            "The oldest is the best"
        )
        child2 = LeafNode(
            "div",
            "The youngest gets the spoils"
        )
        parent_node1 = ParentNode("span", [child1, child2])
        parent_node2 = ParentNode("span", [child2, child1])
        self.assertNotEqual(parent_node1, parent_node2)

    def test_to_html_with_grandchildren(self):
        great_grandchild_node = LeafNode(
            "b",
            "great grandchild",
            {"href": "https://boot.dev"}
        )
        grandchild_node = ParentNode(
            "span",
            [great_grandchild_node]
        )
        child_node = ParentNode(
            "p",
            [grandchild_node],
            {"src": "https://youtube.com", "alt": "Youtube"}
        )
        parent_node = ParentNode(
            "div",
            [child_node],
            {"src": "https://www.google.com"}
        )
        self.assertEqual(
            parent_node.to_html(),
            '<div src="https://www.google.com">'
            '<p src="https://youtube.com" alt="Youtube">'
            '<span>'
            '<b href="https://boot.dev">great grandchild</b>'
            '</span></p></div>'
        )

    def test_no_tag(self):
        leaf_node = LeafNode(
            "p",
            "Plain text paragraph - no links."
        )
        with self.assertRaises(ValueError) as cm:
            ParentNode(None, [leaf_node]).to_html()
        self.assertEqual(
            str(cm.exception),
            "All parent nodes must have a tag."
        )

    def test_no_children(self):
        with self.assertRaises(ValueError) as cm:
            ParentNode("b", None, {"href": "https://www.google.com"}).to_html()
        self.assertEqual(
            str(cm.exception),
            "All parent nodes must have at least 1 child."
        )

    def test_weird_children(self):
        good_child = LeafNode(
            "p",
            "Plain text paragraph - no links."
        )
        bad_child = "Plain text. Not an HTML node."
        with self.assertRaises(ValueError) as cm:
            ParentNode("b", [good_child, bad_child]).to_html()
        self.assertEqual(
            str(cm.exception),
            "Children must be HTMLNode Objects"
        )


class TestTextNodeConversion(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italics(self):
        node = TextNode("This is a italics node", TextType.ITALICS)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italics node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode(
            "This is a link node",
            TextType.LINKS,
            "https://www.google.com"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_image(self):
        node = TextNode(
            "This is an image node",
            TextType.IMAGES,
            "https://www.google.com"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {
                "src": "https://www.google.com",
                "alt": "This is an image node"
            }
        )

    def test_break(self):
        node = TextNode(
            "This is an image node",
            "PHONE",
            "https://www.google.com"
        )
        with self.assertRaises(Exception) as cm:
            text_node_to_html_node(node)
        self.assertEqual(
            str(cm.exception),
            "Not a valid text node type."
        )
