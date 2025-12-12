from textnode import TextType, TextNode


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
