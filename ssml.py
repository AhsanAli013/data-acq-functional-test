

def parse_ssml(ssml: str) -> SSMLNode:
    """
    A minimal SSML parser (no external XML libraries allowed).
    Handles:
        - text nodes
        - tags with attributes
        - nested tags
    """

    i = 0
    n = len(ssml)

    def skip_whitespace():
        nonlocal i
        while i < n and ssml[i].isspace():
            i += 1

    def parse_text() -> SSMLText:
        start = i
        while i < n and ssml[i] != "<":
            i += 1
        return SSMLText(ssml[start:i])

    def parse_tag() -> SSMLTag:
        nonlocal i
        assert ssml[i] == "<"
        i += 1  # skip '<'

        # Read tag name
        start = i
        while i < n and ssml[i].isalnum():
            i += 1
        tag_name = ssml[start:i]

        attributes = {}

        # Parse attributes until '>' or '/>'
        while i < n and ssml[i] not in [">", "/"]:
            skip_whitespace()
            if ssml[i] in [">", "/"]:
                break

            # Read attribute name
            start = i
            while i < n and ssml[i].isalnum():
                i += 1
            attr_name = ssml[start:i]

            skip_whitespace()
            assert ssml[i] == "="
            i += 1
            skip_whitespace()

            # Read quoted attribute value
            quote = ssml[i]
            i += 1
            start = i
            while i < n and ssml[i] != quote:
                i += 1
            attr_value = ssml[start:i]
            i += 1  # skip closing quote

            attributes[attr_name] = attr_value

        # Self closing tag <tag ... />
        if ssml[i] == "/":
            i += 2  # skip "/>"
            return SSMLTag(tag_name, attributes, [])

        # Skip '>'
        i += 1

        # Parse inner content until closing tag
        children: List[SSMLNode] = []

        while True:
            if ssml.startswith(f"</{tag_name}>", i):
                i += len(tag_name) + 3
                break

            if ssml[i] == "<":
                children.append(parse_tag())
            else:
                children.append(parse_text())

        return SSMLTag(tag_name, attributes, children)

    # Entry point: SSML must be a root <speak> tag
    skip_whitespace()
    if ssml[i] != "<":
        raise ValueError("SSML must start with a tag")

    return parse_tag()


def ssml_node_to_text(node: SSMLNode) -> str:
    """
    Recursively extracts *plain text* from the SSML node tree.
    """
    if isinstance(node, SSMLText):
        return node.text

    # For tags: just concatenate children text
    result = ""
    for child in node.children:
        result += ssml_node_to_text(child)

    return result
