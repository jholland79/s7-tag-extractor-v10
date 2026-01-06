"""S7 project structure navigation."""

from pathlib import Path

SYMLIST_PATTERN = "**/SYMLIST.DBF"


class S7Project:
    """Navigate and extract information from S7 project files."""

    def __init__(self, s7p_file: Path) -> None:
        """Initialize with an S7 project file path."""
        self.s7p_file = Path(s7p_file)
        self.project_dir = self.s7p_file.parent

    def find_symlist_files(self) -> list[Path]:
        """Find all SYMLIST.DBF files in the project."""
        return list(self.project_dir.glob(SYMLIST_PATTERN))
