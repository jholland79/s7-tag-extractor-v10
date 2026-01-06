"""Parser for SYMLIST.DBF symbol tables."""

from dataclasses import dataclass
from pathlib import Path

# This will be mocked in tests
DBF = None


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
    symbols = []
    table = DBF(str(symlist_path))

    for record in table:
        symbol = Symbol(
            name=record["_SKZ"],
            address=record["_OPHIST"],
            comment=record["_COMMENT"],
        )
        symbols.append(symbol)

    return symbols
