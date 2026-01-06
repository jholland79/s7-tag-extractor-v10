"""Data models for tag extraction."""

from dataclasses import dataclass


@dataclass
class Tag:
    """Represents a PLC tag."""

    name: str
    address: str
    data_type: str


@dataclass
class PiTypeMapping:
    """Represents a mapping from S7 type to PI point type."""

    point_type: str
    location2: int
