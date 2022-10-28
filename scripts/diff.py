"""
This file process difference between two easylist rule-set, and record into a json file.
"""
import argparse
import json
import sys
from itertools import pairwise
from pathlib import Path
from typing import Any, Dict

from attrs import asdict

SCRIPT_PATH = Path(__file__)
SCRIPT_DIR = SCRIPT_PATH.parent
PROJECT_DIR = SCRIPT_DIR.parent
SRC_DIR = PROJECT_DIR / "src"

sys.path.append(str(SRC_DIR))

import repo_utils
from filter_parser import Rule, Rules

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


def rules_diff(new_rules: Rules, old_rules: Rules) -> Dict[str, Any]:
    # TODO
    def rules_contain(rules: Rules, checked_rule: Rule) -> bool:
        pass

    added_rules = [
        asdict(rule) for rule in new_rules if not rules_contain(old_rules, rule)
    ]
    deleted_rules = [
        asdict(rule) for rule in old_rules if not rules_contain(new_rules, rule)
    ]
    return {
        "added": added_rules,
        "deleted": deleted_rules,
    }


def main():
    args = parser.parse_args()
    repo = repo_utils.get_git_repo(args.repo_dir)
    all_rules_iter = repo_utils.iter_all_rules_from_repo(
        repo, args.rel_filepath, count=args.count
    )
    with all_rules_iter:
        for new_rules, old_rules in pairwise(all_rules_iter):
            new_rules: Rules
            old_rules: Rules
            diffs = rules_diff(new_rules, old_rules)
            # TODO
    pass


if __name__ == "__main__":
    main()
