"""
Utilities for analyzing majestic million data.
"""
import pandas as pd
from pathlib import Path

SCRIPT_PATH = Path(__file__)
SCRIPT_DIR = SCRIPT_PATH.parent
PROJECT_DIR = SCRIPT_DIR.parent
DEFAULT_MAJESTIC_PATH = PROJECT_DIR / ".cache" / "download" / "majestic_million.csv"


def load_majestic(path: Path = DEFAULT_MAJESTIC_PATH) -> pd.DataFrame:
    assert path.exists(), f"Majestic file does not exist: {path}. Try to run `scripts/download_majestic.py` first."
    return pd.read_csv(path)


def find_majestic_rank_entry_by_domain(domain: str, majestic_df: pd.DataFrame) -> pd.DataFrame:
    """
    Find the entry of the specified domain in majestic million.
    """
    return majestic_df[majestic_df["Domain"] == domain]
