"""Tests for BAUSTEIN.DBF data block parsing."""

from pathlib import Path
from unittest.mock import MagicMock, patch

from s7_tag_extractor_v10.parser.blocks import parse_blocks


class TestParseBlocks:
    """Tests for parse_blocks function."""

    def test_parse_blocks_extracts_data_block_with_element_type(self) -> None:
        """Parsing BAUSTEIN.DBF extracts data block definitions with element types."""
        # Arrange
        mock_record = MagicMock()
        mock_record.__getitem__ = lambda self, key: {
            "_NUMMER": 100,
            "_TYP": "DB",
            "_DATEN": b"\x10\x00Motor_Speed\x00REAL\x00",
        }[key]

        mock_table = MagicMock()
        mock_table.__iter__ = lambda self: iter([mock_record])

        baustein_path = Path("/fake/BAUSTEIN.DBF")

        # Act
        with patch("s7_tag_extractor_v10.parser.blocks.DBF", return_value=mock_table):
            blocks = parse_blocks(baustein_path)

        # Assert
        assert len(blocks) == 1
        assert blocks[0].number == 100
        assert blocks[0].block_type == "DB"
        assert len(blocks[0].elements) == 1
        assert blocks[0].elements[0].name == "Motor_Speed"
        assert blocks[0].elements[0].data_type == "REAL"
