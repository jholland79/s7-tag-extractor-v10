"""Data models for tag extraction."""

from dataclasses import dataclass


@dataclass
class Tag:
    """Represents a PLC tag."""

    name: str
    address: str
    data_type: str
