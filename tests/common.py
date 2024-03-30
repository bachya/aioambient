"""Define common test utilities."""

from pathlib import Path

TEST_API_KEY = "12345abcde"
TEST_APP_KEY = "12345abcde"
TEST_MAC = "12:34:56:78:90:AB"


def load_fixture(filename: str) -> str:
    """Load a fixture.

    Args:
    ----
        filename: The filename of the fixtures/ file to load.

    Returns:
    -------
        A string containing the contents of the file.

    """
    path = Path(f"{Path(__file__).parent}/fixtures/{filename}")
    with Path.open(path, encoding="utf-8") as fptr:
        return fptr.read()
