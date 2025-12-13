import re
import pdb  # noqa F401


def extract_markdown_images(text):
    markdown_image_list = []
    markdown_image_list.extend(
        re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    )
    return markdown_image_list


def extract_markdown_links(text):
    markdown_link_list = []
    markdown_link_list.extend(
        re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    )
    return markdown_link_list
