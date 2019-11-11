import shutil
from pathlib import Path
import re

from git import Repo


def get_file_history(repository_path, file_path, is_url=False, branch_name="master", tmp_dir="tmp", clean=True):
    """
    Returns a list containing strings of the historical modifications of a file
    from a given git repository (locally only).

    Args:
        repository_path (str): The path to a git repository (i.e. containing a .git folder).
        file_path (str): The path to a desired file within repository_path.
        is_url (bool): If True, the program expect a remote Git URL.
        branch_name (str): The branch name from which you want to fetch the textual history of your file.
        tmp_dir (str): The path of the folder in which to clone the remote repository.
        clean (bool): If True, clean the downloaded repository after fetching data.

    Returns:
        List[str]: The list containing the iterations of your file.

    """
    print(is_url)
    if is_url:
        # Remote git repository case
        # This regex checks for most of GitHub and GitLab URL viability.
        online_git_repo_regex = r"((git|ssh|http(s)?)|(git@[\w\.]+))(:(\/\/)?)" \
                                r"([\w\.@\:\-~\/]+\/)([\w\.@\:\-~]+)(\.git)(\/)?"

        url_match = re.findall(online_git_repo_regex, repository_path)
        repo_name = url_match[0][7]  # Keep the name of the repo
        repo = Repo.clone_from(repository_path, f"{tmp_dir}/{repo_name}")
    else:
        # Local git repository case
        repository_path = Path(repository_path)
        repo = Repo(repository_path)

    commits = reversed(list(repo.iter_commits(branch_name, paths=file_path)))

    diffs = [
        repo.git.show(f'{commit.hexsha}:{file_path}')
        for commit in commits
    ]

    if is_url and clean:
        shutil.rmtree(f"{tmp_dir}/{repo_name}")

    return diffs
