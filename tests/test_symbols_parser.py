"""Tests for SYMLIST.DBF symbol table parsing."""

from pathlib import Path
from unittest.mock import MagicMock, patch

from s7_tag_extractor_v10.parser.symbols import parse_symlist


class TestParseSymlist:
    """Tests for parse_symlist function."""

    def test_parse_symlist_extracts_symbol_name_address_comment(self) -> None:
        """Parsing SYMLIST.DBF extracts name, address, comment from each record."""
        # Arrange
        mock_record = MagicMock()
        mock_record.__getitem__ = lambda self, key: {
            "_SKZ": "Motor1",
            "_OPHIST": "M0.0",
            "_COMMENT": "Main motor status",
        }[key]

        mock_table = MagicMock()
        mock_table.__iter__ = lambda self: iter([mock_record])

        symlist_path = Path("/fake/SYMLIST.DBF")

        # Act
        with patch("s7_tag_extractor_v10.parser.symbols.DBF", return_value=mock_table):
            symbols = parse_symlist(symlist_path)

        # Assert
        assert len(symbols) == 1
        assert symbols[0].name == "Motor1"
        assert symbols[0].address == "M0.0"
        assert symbols[0].comment == "Main motor status"
