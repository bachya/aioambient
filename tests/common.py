"""Define common test utilities."""
import os

TEST_API_KEY = "12345abcde"
TEST_APP_KEY = "12345abcde"
TEST_MAC = "12:34:56:78:90:AB"


def load_fixture(filename):
    """Load a fixture."""
    path = os.path.join(os.path.dirname(__file__), "fixtures", filename)
    with open(path, encoding="utf-8") as fptr:
        return fptr.read()
