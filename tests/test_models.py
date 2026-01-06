"""Tests for data models: Tag, Symbol, DataBlock."""

from s7_tag_extractor_v10.models import Tag


class TestTag:
    """Tests for the Tag dataclass."""

    def test_create_tag_with_required_fields_stores_values(self) -> None:
        """Creating a Tag with required fields stores them correctly."""
        # Arrange
        name = "Motor1_Run"
        address = "DB100.DBX4.0"
        data_type = "BOOL"

        # Act
        tag = Tag(name=name, address=address, data_type=data_type)

        # Assert
        assert tag.name == name
        assert tag.address == address
        assert tag.data_type == data_type
