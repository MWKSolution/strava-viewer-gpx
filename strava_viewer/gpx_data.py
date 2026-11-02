import xml.etree.ElementTree as ET

GPX_NAMESPACES = {
    "http://www.topografix.com/GPX/1/1",
    "http://www.topografix.com/GPX/1/0",
}

def is_gpx(filepath: str) -> bool:
    """Check if given file has GPX header"""
    try:
        tree = ET.parse(filepath)
    except ET.ParseError as e:
        print(f"Not well-formed XML: {e}")
        return False

    root = tree.getroot()
    # Check root tag is 'gpx' (strip namespace for comparison)
    tag = root.tag.split("}")[-1] if "}" in root.tag else root.tag
    if tag != "gpx":
        print(f"Root element is <{tag}>, not <gpx>")
        return False
    # Check namespace
    ns = root.tag.split("}")[0].lstrip("{") if "}" in root.tag else None
    if ns not in GPX_NAMESPACES:
        print(f"Namespace '{ns}' is not a valid GPX namespace")
        return False
    # Check version attribute
    version = root.get("version")
    if version not in ("1.0", "1.1"):
        print(f"Invalid or missing version: '{version}'")
        return False

    print(f"Valid GPX {version} document")
    return True
