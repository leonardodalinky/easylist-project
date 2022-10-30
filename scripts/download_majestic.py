"""
Script for downloading majestic million data from https://majestic.com/reports/majestic-million
"""
import wget
import argparse
from pathlib import Path

SCRIPT_PATH = Path(__file__)
SCRIPT_DIR = SCRIPT_PATH.parent
PROJECT_DIR = SCRIPT_DIR.parent


parser = argparse.ArgumentParser(description="Download majestic million data")
parser.add_argument("-o", "--output", type=Path, default=PROJECT_DIR / ".cache" / "download" / "majestic_million.csv",
                    help="Output file path. Default to $PROJECT_DIR/tmp_download/majestic_million.csv")


if __name__ == "__main__":
    args = parser.parse_args()
    output_path: Path = args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    url = "https://downloads.majestic.com/majestic_million.csv"
    wget.download(url, out=str(output_path))
