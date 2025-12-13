import unittest
from conversions.extract_text import extract_markdown_images


class TestDelimiterSplits(unittest.TestCase):
    def test_image(self):
        # Image case
        text = "This is text with an image ![image](https://i.imgur.com/zjjcJKZ.png)"  # noqa E501
        matches = extract_markdown_images(text)
        expected_matches = [
            ("image", "https://i.imgur.com/zjjcJKZ.png")
        ]
        self.assertListEqual(expected_matches, matches)

        # Double image case
        text = "This is text with two images ![image](https://i.imgur.com/zjjcJKZ.png) ![image2](https://boot.dev/image)"  # noqa E501
        matches = extract_markdown_images(text)
        expected_matches = [
            ("image", "https://i.imgur.com/zjjcJKZ.png"),
            ("image2", "https://boot.dev/image")
        ]
        self.assertListEqual(expected_matches, matches)

        # Nested image case (shouldn't happen, but hey...)
        text = "This is text with two images ![image](https://i.imgur.![image2](https://boot.dev/image)com/zjjcJKZ.png)"  # noqa E501
        matches = extract_markdown_images(text)
        expected_matches = [
            ("image2", "https://boot.dev/image")
        ]
        self.assertListEqual(expected_matches, matches)

    def test_link(self):
        # Link case
        text = "This is text with a link [image](https://i.imgur.com/zjjcJKZ.png)"  # noqa E501
        matches = extract_markdown_images(text)
        expected_matches = [
            ("image", "https://i.imgur.com/zjjcJKZ.png")
        ]
        self.assertListEqual(expected_matches, matches)

    def test_combined(self):
        # Double image and a link case
        text = "This is text with two images ![image](https://i.imgur.com/zjjcJKZ.png) ![image2](https://boot.dev/image) and a link [link](https://aol.com)"  # noqa E501
        matches = extract_markdown_images(text)
        expected_matches = [
            ("image", "https://i.imgur.com/zjjcJKZ.png"),
            ("image2", "https://boot.dev/image"),
            ("link", "https://aol.com")
        ]
        self.assertListEqual(expected_matches, matches)
