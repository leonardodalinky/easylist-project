"""
Utilities for repo manipulations.
"""
from os import PathLike
from git.repo import Repo
from pathlib import Path
from typing import Union

from filter_parser import Rules


def get_git_repo(git_repo_dir: Union[str, PathLike]):
    git_repo_dir = Path(git_repo_dir)
    assert git_repo_dir.exists() and git_repo_dir.is_dir(), f"Directory not found: {git_repo_dir}"
    git_repo = Repo(git_repo_dir)
    assert not git_repo.bare, f"Could not find .git under directory: {git_repo_dir}"
    return git_repo


def get_rules_rel_from_repo(repo: Repo, rel_filepath: Union[str, PathLike]):
    comm = repo.head.commit
    assert repo.working_tree_dir is not None
    return Rules.from_file(Path(repo.working_tree_dir) / rel_filepath, comm.committed_datetime)


def iter_all_rule_sets_from_repo(repo: Repo, rel_filepath: Union[str, PathLike]):
    origin_comm = repo.head.commit
    try:
        for comm in list(repo.iter_commits()):
            repo.head.set_reference(comm)
            yield get_rules_rel_from_repo(repo, rel_filepath)
    finally:
        repo.head.set_commit(origin_comm)

