"""Tests for array tag expansion."""

from s7_tag_extractor_v10.parser.arrays import expand_array
from s7_tag_extractor_v10.parser.blocks import BlockElement


class TestExpandArray:
    """Tests for expand_array function."""

    def test_expand_array_creates_individual_tags_with_correct_addresses(self) -> None:
        """Array[0..9] of INT expands to 10 individual tags with correct addresses."""
        # Arrange
        element = BlockElement(name="Motor_Speeds", data_type="Array[0..9] of INT")
        db_number = 100
        base_offset = 0

        # Act
        tags = expand_array(element, db_number, base_offset)

        # Assert
        assert len(tags) == 10
        assert tags[0].name == "Motor_Speeds[0]"
        assert tags[0].address == "DB100.DBW0"
        assert tags[0].data_type == "INT"
        assert tags[9].name == "Motor_Speeds[9]"
        assert tags[9].address == "DB100.DBW18"
        assert tags[9].data_type == "INT"
