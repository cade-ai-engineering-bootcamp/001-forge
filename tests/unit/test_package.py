from importlib.metadata import version

import forge


def test_package_identity() -> None:
    assert forge.__name__ == "forge"
    assert version("forge-ai-starter-kit") == "0.1.0"
