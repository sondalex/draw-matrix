from pathlib import Path
import pytest
import numpy as np


@pytest.fixture(scope="session")
def fixtures_path() -> Path:
    path = Path(__file__)
    return path.parent / "fixtures"


@pytest.fixture(scope="module")
def matrix() -> np.array:
    m = np.array([
        [0, 1],
        [2, 1]
    ])
    return m
