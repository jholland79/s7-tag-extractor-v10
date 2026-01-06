"""Parser for BAUSTEIN.DBF data block definitions."""

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# This will be mocked in tests; typed as Callable to satisfy type checker
DBF: Callable[[str], Any] = None  # type: ignore[assignment]

# DBF field names for BAUSTEIN.DBF
FIELD_NUMBER = "_NUMMER"
FIELD_TYPE = "_TYP"
FIELD_DATA = "_DATEN"


@dataclass
class BlockElement:
    """Represents an element within a data block."""

    name: str
    data_type: str


@dataclass
class Block:
    """Represents a PLC data block."""

    number: int
    block_type: str
    elements: list[BlockElement]


def parse_blocks(baustein_path: Path) -> list[Block]:
    """Parse a BAUSTEIN.DBF file and extract data block definitions.

    Args:
        baustein_path: Path to the BAUSTEIN.DBF file.

    Returns:
        A list of Block objects extracted from the file.
    """
    table = DBF(str(baustein_path))
    blocks = []

    for record in table:
        number = record[FIELD_NUMBER]
        block_type = record[FIELD_TYPE]
        data = record[FIELD_DATA]

        elements = _parse_block_elements(data)
        blocks.append(Block(number=number, block_type=block_type, elements=elements))

    return blocks


def _parse_block_elements(data: bytes) -> list[BlockElement]:
    """Parse block elements from binary data.

    Args:
        data: Binary data containing element definitions.

    Returns:
        A list of BlockElement objects.
    """
    elements = []
    offset = 0

    while offset < len(data):
        # Skip metadata byte if present at offset
        if offset < len(data) and data[offset : offset + 2] == b"\x10\x00":
            offset += 2
        elif offset < len(data) and data[offset] == 0:
            # Skip single null bytes
            offset += 1
            continue

        # Read element name (null-terminated string)
        name_end = data.find(b"\x00", offset)
        if name_end == -1 or name_end == offset:
            break

        name = data[offset:name_end].decode("utf-8", errors="replace")
        if not name:  # Skip empty names
            offset = name_end + 1
            continue

        offset = name_end + 1

        # Read data type (null-terminated string)
        type_end = data.find(b"\x00", offset)
        if type_end == -1:
            break

        data_type = data[offset:type_end].decode("utf-8", errors="replace")
        offset = type_end + 1

        elements.append(BlockElement(name=name, data_type=data_type))

    return elements
