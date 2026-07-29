class HTMLNode:
    def __init__(self, tag: str | None = None, value: str | None = None, children: list | None = None, props: dict[str, str] | None = None) -> None:
        self.tag: str | None = tag
        self.value: str | None = value
        self.children: list | None = children
        self.props: dict[str, str] | None = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        final_html = ""
        if self.props != None:
            for key, val in self.props.items():
                final_html += f" {key}=\"{val}\""
        return final_html

    def __repr__(self) -> str:
        return (
            f"Tag: {self.tag}\n" +
            f"Value: {self.value}\n" +
            f"Children: {self.children}\n" +
            f"Props: {self.props}\n"
        )
