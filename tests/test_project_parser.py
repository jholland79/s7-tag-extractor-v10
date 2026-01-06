"""Tests for S7 project structure navigation."""

from pathlib import Path

from s7_tag_extractor_v10.parser.project import S7Project


class TestS7Project:
    """Tests for S7 project navigation."""

    def test_find_symlist_dbf_returns_paths_to_symbol_tables(
        self, tmp_path: Path
    ) -> None:
        """Finding SYMLIST.DBF files returns paths to all symbol tables in project."""
        # Arrange
        project_dir = tmp_path / "sample_project"
        project_dir.mkdir()
        s7p_file = project_dir / "project.s7p"
        s7p_file.touch()

        # Create a nested SYMLIST.DBF file as found in real S7 projects
        ydb_dir = project_dir / "YDBs" / "00000001"
        ydb_dir.mkdir(parents=True)
        symlist_file = ydb_dir / "SYMLIST.DBF"
        symlist_file.touch()

        project = S7Project(s7p_file)

        # Act
        symlist_paths = project.find_symlist_files()

        # Assert
        assert len(symlist_paths) == 1
        assert symlist_paths[0] == symlist_file
