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

# Binary markers in block element data
METADATA_MARKER = b"\x10\x00"
NULL_TERMINATOR = b"\x00"


def _read_null_terminated_string(data: bytes, offset: int) -> tuple[str, int] | None:
    """Read a null-terminated string from binary data.

    Args:
        data: Binary data containing the string.
        offset: Starting position to read from.

    Returns:
        Tuple of (decoded string, new offset after null terminator),
        or None if no valid string found.
    """
    end = data.find(NULL_TERMINATOR, offset)
    if end == -1:
        return None
    value = data[offset:end].decode("utf-8", errors="replace")
    return (value, end + 1)


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
        # Skip metadata marker if present at offset
        if data[offset : offset + 2] == METADATA_MARKER:
            offset += 2
        elif data[offset] == 0:
            # Skip single null bytes
            offset += 1
            continue

        # Read element name (null-terminated string)
        result = _read_null_terminated_string(data, offset)
        if result is None or result[0] == "":
            break

        name, offset = result
        if not name:  # Skip empty names
            continue

        # Read data type (null-terminated string)
        result = _read_null_terminated_string(data, offset)
        if result is None:
            break

        data_type, offset = result

        elements.append(BlockElement(name=name, data_type=data_type))

    return elements
