"""Parser for array tag expansion."""

import re

from s7_tag_extractor_v10.models import Tag
from s7_tag_extractor_v10.parser.blocks import BlockElement

# Regex pattern to parse array declarations e.g., "Array[0..9] of INT"
ARRAY_PATTERN = re.compile(r"Array\[(\d+)\.\.(\d+)\]\s+of\s+(\w+)")

# Size in bytes for S7 data types
TYPE_SIZES = {
    "INT": 2,
    "DINT": 4,
    "REAL": 4,
    "BOOL": 1,
    "BYTE": 1,
    "WORD": 2,
    "DWORD": 4,
}
DEFAULT_TYPE_SIZE = 2


def expand_array(element: BlockElement, db_number: int, base_offset: int) -> list[Tag]:
    """Expand an array element into individual tags with correct addresses.

    Args:
        element: BlockElement representing an array
        db_number: Database number
        base_offset: Base offset in bytes

    Returns:
        List of Tag objects for each array element
    """
    match = ARRAY_PATTERN.search(element.data_type)
    if not match:
        raise ValueError(f"Invalid array data type: {element.data_type}")

    start_idx = int(match.group(1))
    end_idx = int(match.group(2))
    element_type = match.group(3)

    element_size = TYPE_SIZES.get(element_type, DEFAULT_TYPE_SIZE)

    tags = []
    for idx in range(start_idx, end_idx + 1):
        offset = base_offset + (idx - start_idx) * element_size
        tag_name = f"{element.name}[{idx}]"
        tag_address = f"DB{db_number}.DBW{offset}"
        tags.append(Tag(name=tag_name, address=tag_address, data_type=element_type))

    return tags
