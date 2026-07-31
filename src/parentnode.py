from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict[str, str] | None = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None: raise ValueError
        if self.children is None: raise ValueError("Children Missing")
        res = ""
        for children in self.children:
            if children is not None:
                res += children.to_html()
        return f"<{self.tag}{self.props_to_html()}>{res}</{self.tag}>"
