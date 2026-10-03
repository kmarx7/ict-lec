from src.utils.filename import safe_filename


def test_safe_filename_removes_forbidden_characters():
    assert safe_filename(' Week: 04 / "AI" ') == "Week_ 04 _ _AI"

