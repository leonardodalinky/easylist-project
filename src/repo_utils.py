"""
Utilities for repo manipulations.
"""
from os import PathLike
from pathlib import Path
from typing import Union

from git.repo import Repo

from filter_parser import Rules


def get_git_repo(git_repo_dir: Union[str, PathLike]):
    """
    Get `easylistchina` repo object.
    """
    git_repo_dir = Path(git_repo_dir)
    assert (
        git_repo_dir.exists() and git_repo_dir.is_dir()
    ), f"Directory not found: {git_repo_dir}"
    git_repo = Repo(git_repo_dir)
    assert not git_repo.bare, f"Could not find .git under directory: {git_repo_dir}"
    return git_repo


def get_rules_rel_from_repo(repo: Repo, rel_filepath: Union[str, PathLike]):
    comm = repo.head.commit
    assert repo.working_tree_dir is not None
    return Rules.from_file(
        Path(repo.working_tree_dir) / rel_filepath, comm.committed_datetime, commit_hash=comm.hexsha
    )


def iter_all_rules_from_repo(
    repo: Repo, rel_filepath: Union[str, PathLike], count=None
):
    """
    Iterate all previous commits of the file and parse.

    Args:
        repo:
        rel_filepath:
        count: If None, iterate all commits. Otherwise, iterate the latest `count` commits.

    Returns:

    """

    return _RulesIterator(repo, rel_filepath, count=count)


class _RulesIterator:
    def __init__(self, repo, rel_filepath, count=None):
        self.repo = repo
        self.origin_comm = repo.head.commit
        self.rel_filepath = rel_filepath
        self.count = count
        self.commits = list(repo.iter_commits(paths=rel_filepath))
        self.index = 0

    def __len__(self):
        return len(self.commits)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.commits) or (self.count is not None and self.index >= self.count):
            self.repo.head.set_commit(self.origin_comm)
            raise StopIteration
        comm = self.commits[self.index]
        self.repo.head.set_commit(comm)
        self.index += 1
        return get_rules_rel_from_repo(self.repo, self.rel_filepath)

    def __del__(self):
        self.repo.head.set_commit(self.origin_comm)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.repo.head.set_commit(self.origin_comm)
