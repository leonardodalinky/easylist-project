"""
This file extract all historical easylist rules from a git repo.
"""
import argparse
import os
import shutil
import sys
import warnings
from pathlib import Path

from diff import HASH_LEN
from tqdm import tqdm

SCRIPT_PATH = Path(__file__)
SCRIPT_DIR = SCRIPT_PATH.parent
PROJECT_DIR = SCRIPT_DIR.parent
SRC_DIR = PROJECT_DIR / "src"

sys.path.append(str(SRC_DIR))

import repo_utils
from filter_parser import Rules

parser = argparse.ArgumentParser()
parser.add_argument(
    "-r",
    "--repo-dir",
    type=Path,
    required=True,
    dest="repo_dir",
    help="The directory of the git repo",
)
parser.add_argument(
    "-f",
    "--rel-path",
    type=Path,
    required=True,
    dest="rel_filepath",
    help="The relative path of the file to compare",
)
parser.add_argument(
    "-o",
    "--output-dir",
    type=Path,
    required=True,
    dest="output_dir",
    help="The directory to save the output json file",
)
parser.add_argument(
    "-c",
    "--count",
    type=int,
    dest="count",
    default=None,
    help="The number of commits to compare. If not given, compare all commits.",
)


def main():
    args = parser.parse_args()
    repo_dir: Path = args.repo_dir
    repo = repo_utils.get_git_repo(repo_dir)
    rel_filepath: Path = args.rel_filepath
    all_rules_iter = repo_utils.iter_all_rules_from_repo(
        repo, args.rel_filepath, count=args.count
    )
    # create dir if not exists
    output_dir = Path(args.output_dir)
    if not output_dir.exists():
        output_dir.mkdir(parents=True)
    if os.listdir(output_dir):
        warnings.warn(f"Output dir is not empty: {output_dir}")

    with all_rules_iter:
        for i, rules in enumerate(tqdm(all_rules_iter)):
            rules: Rules
            shutil.copy(
                repo_dir / rel_filepath,
                output_dir
                / f"{i:05}_{rules.commit_hash[:HASH_LEN]}_{int(rules.time.timestamp())}.txt",
            )


if __name__ == "__main__":
    main()
