from htmlnode import HTMLNode
from typing import override

class LeafNode(HTMLNode):

    def __init__(self, tag: str | None = None, value: str | None = None, children: list | None = None, props: dict[str, str] | None = None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError

        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    @override
    def __repr__(self) -> str:
        return f"Tag: \"{self.tag}\" | Value: \"{self.value}\"| Props: \"{self.props}\""
