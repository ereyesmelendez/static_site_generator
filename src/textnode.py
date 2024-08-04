text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

class TextNode:
    def __init__(self, text, text_type, url=None, href=None, src=None, alt=None, value=None):
        self.text = text
        self.text_type = text_type
        self.url = url
        self.href = href
        self.src = src
        self.alt = alt
        self.value = value

    def __eq__(self, other):
        if isinstance(other, TextNode):
            print("Comparing:", self, other)  # Add this line
            return (
                self.text == other.text and
                self.text_type == other.text_type and
                self.url == other.url
            )
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"