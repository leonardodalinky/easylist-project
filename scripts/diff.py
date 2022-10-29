"""
This file process difference between two easylist rule-set, and record into a json file.
"""
import argparse
import json
import os
import re
import sys
import warnings
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Tuple
from joblib import Parallel, delayed

from attrs import asdict
from tqdm import tqdm

SCRIPT_PATH = Path(__file__)
SCRIPT_DIR = SCRIPT_PATH.parent
PROJECT_DIR = SCRIPT_DIR.parent
SRC_DIR = PROJECT_DIR / "src"

sys.path.append(str(SRC_DIR))

from filter_parser import Rules

HASH_LEN = 9

parser = argparse.ArgumentParser()
parser.add_argument(
    "-d",
    "--easylist-dir",
    type=Path,
    required=True,
    dest="easylist_dir",
    help="The directory of the all easylists extracted by `extract_easylists.py`",
)
parser.add_argument(
    "-o",
    "--output-dir",
    type=Path,
    required=True,
    dest="output_dir",
    help="The directory to save the output json file",
)


def rules_diff(new_rules: Rules, old_rules: Rules) -> Dict[str, Any]:
    added_rules = [asdict(rule) for rule in new_rules if rule not in old_rules]
    deleted_rules = [asdict(rule) for rule in old_rules if rule not in new_rules]
    return {
        "added": added_rules,
        "deleted": deleted_rules,
    }


def main():
    args = parser.parse_args()
    easylist_dir: Path = args.easylist_dir
    assert (
        easylist_dir.exists() and easylist_dir.is_dir()
    ), f"Easylist dir does not exist: {easylist_dir}"
    # create dir if not exists
    output_dir = Path(args.output_dir)
    if not output_dir.exists():
        output_dir.mkdir(parents=True)
    if os.listdir(output_dir):
        warnings.warn(f"Output dir is not empty: {output_dir}")

    name_re = re.compile(rf"(\d{{5}})_(.{{{HASH_LEN}}})_(\d+)\.txt")
    easylist_files = list(sorted(filter(name_re.match, os.listdir(easylist_dir))))
    easylist_files_pairs = tuple((easylist_files[i], easylist_files[i + 1]) for i in range(len(easylist_files) - 1))

    def process_diff(pair: Tuple[str, str]):
        new_file, old_file = pair
        new_file_match = name_re.match(new_file)
        old_file_match = name_re.match(old_file)
        new_file_idx = int(new_file_match.group(1))
        old_file_idx = int(old_file_match.group(1))
        new_file_hash = new_file_match.group(2)
        old_file_hash = old_file_match.group(2)
        new_file_ts = int(new_file_match.group(3))
        old_file_ts = int(old_file_match.group(3))

        new_rules = Rules.from_file(
            easylist_dir / new_file,
            datetime.utcfromtimestamp(new_file_ts),
            new_file_hash,
            )
        old_rules = Rules.from_file(
            easylist_dir / old_file,
            datetime.utcfromtimestamp(old_file_ts),
            old_file_hash,
            )
        diff = rules_diff(new_rules, old_rules)
        output_file = output_dir / f"{new_file_idx:05}_{old_file_idx:05}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(diff, f, indent=2, ensure_ascii=False)

    Parallel(n_jobs=-1)(delayed(process_diff)(pair) for pair in tqdm(easylist_files_pairs))


if __name__ == "__main__":
    main()
