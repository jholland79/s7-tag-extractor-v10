"""Parser for SYMLIST.DBF symbol tables."""

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# This will be mocked in tests; typed as Callable to satisfy type checker
DBF: Callable[[str], Any] = None  # type: ignore[assignment]

# DBF field names for SYMLIST.DBF
FIELD_NAME = "_SKZ"
FIELD_ADDRESS = "_OPHIST"
FIELD_COMMENT = "_COMMENT"


@dataclass
class Symbol:
    """Represents a PLC symbol."""

    name: str
    address: str
    comment: str


def parse_symlist(symlist_path: Path) -> list[Symbol]:
    """Parse a SYMLIST.DBF file and extract symbols.

    Args:
        symlist_path: Path to the SYMLIST.DBF file.

    Returns:
        A list of Symbol objects extracted from the file.
    """
    table = DBF(str(symlist_path))

    return [
        Symbol(
            name=record[FIELD_NAME],
            address=record[FIELD_ADDRESS],
            comment=record[FIELD_COMMENT],
        )
        for record in table
    ]
