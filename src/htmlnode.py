class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props:
            total_string = ""
            for key in self.props:
                total_string += f' {key}="{self.props[key]}"'

            return total_string
        return ""

    def __eq__(self, other):
        if (
            (self.tag == other.tag)
            and (self.value == other.value)
            and (self.children == other.children)
            and (self.props == other.props)
        ):
            return True
        return False

    def __repr__(self):
        return f"HTMLNode(Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props})"  # noqa E501


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value

        prop_text = self.props_to_html()
        starting_tag = f"<{self.tag}{prop_text}>"
        ending_tag = f"</{self.tag}>"

        return f"{starting_tag}{self.value}{ending_tag}"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag.")
        if self.children is None:
            raise ValueError("All parent nodes must have at least 1 child.")

        prop_text = self.props_to_html()
        starting_tag = f"<{self.tag}{prop_text}>"
        ending_tag = f"</{self.tag}>"
        children_text = ""
        for child in self.children:
            if not isinstance(child, HTMLNode):
                raise ValueError("Children must be HTMLNode Objects")
            children_text += child.to_html()

        return starting_tag + children_text + ending_tag
