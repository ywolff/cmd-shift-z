from git import Repo
from pathlib import Path


def get_file_data(repository_path, file_path, branch_name="master"):
    """
    Returns a list containing strings of the historical modifications of a file
    from a given git repository.

    Args:
        repository_path (str): The path to a git repository (i.e. containing a .git folder).
        file_path (str): The path to a desired file within repository_path.
        branch_name (str): The branch name from which you want to fetch the textual history of your file.

    Returns:
        file_history (list): The list containing the iterations of your file.

    """
    if not isinstance(repository_path, Path):
        repository_path = Path(repository_path)

    repo = Repo(repository_path)
    commits = list(repo.iter_commits(branch_name, paths=file_path))
    file_history = []

    for commit in commits:
        # For each commit of the given branch name,
        # get the content of the file and add it to file_history.
        file_content = repo.git.show('{}:{}'.format(commit.hexsha, file_path))
        file_history.append(file_content)

    return file_history
