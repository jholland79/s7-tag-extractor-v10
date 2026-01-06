"""Type mapping from S7 to PI point types."""

from s7_tag_extractor_v10.models import PiTypeMapping


def map_s7_type_to_pi(s7_type: str) -> PiTypeMapping:
    """Map S7 type to PI point type.

    Args:
        s7_type: The S7 data type name

    Returns:
        PiTypeMapping with point_type and location2
    """
    if s7_type == "BOOL":
        return PiTypeMapping(point_type="Int16", location2=2)
    raise ValueError(f"Unsupported type: {s7_type}")
