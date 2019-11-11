from git import Repo
from pathlib import Path


def get_file_history(repository_path, file_path, branch_name="master"):
    """
    Returns a list containing strings of the historical modifications of a file
    from a given git repository (locally only).

    Args:
        repository_path (str): The path to a git repository (i.e. containing a .git folder).
        file_path (str): The path to a desired file within repository_path.
        branch_name (str): The branch name from which you want to fetch the textual history of your file.

    Returns:
        List[str]: The list containing the iterations of your file.

    """
    repository_path = Path(repository_path)

    repo = Repo(repository_path)
    commits = reversed(list(repo.iter_commits(branch_name, paths=file_path)))
    return [
        repo.git.show(f'{commit.hexsha}:{file_path}')
        for commit in commits
    ]
