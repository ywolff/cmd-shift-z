import shutil
import sys
from pathlib import Path
import re

from git import Repo, remote
from tqdm import tqdm, trange


# pbar = tqdm(total=100)


def get_file_history(repository, file_path, branch_name="master", tmp_dir="tmp", clean=True):
    """
    Returns a list containing strings of the historical modifications of a file
    from a given git repository (locally only).

    Args:
        repository (str): The source to a git repository, either an url or a local path.
        file_path (str): The path to a desired file within repository.
        branch_name (str): The branch name from which you want to fetch the textual history of your file.
        tmp_dir (str): The path of the folder in which to clone the remote repository.
        clean (bool): If True, clean the downloaded repository after fetching data.

    Returns:
        List[str]: The list containing the iterations of your file.

    """
    repository_name, repository = get_git_repository_and_name(repository, tmp_dir)
    commits = reversed(list(repository.iter_commits(branch_name, paths=file_path)))

    diffs = [
        repository.git.show(f'{commit.hexsha}:{file_path}')
        for commit in commits
    ]

    if clean:
        try:
            shutil.rmtree(f"{tmp_dir}/{repository_name}")
        except FileNotFoundError:
            pass

    return diffs


def get_git_repository_and_name(repository_source, tmp_dir):
    """
    Returns two things, the name of the repository taken from the folder name if local or the project name if remote,
    and the repository object itself (git.Repo) from the GitPython library.
    Args:
        repository_source (str): The source to a git repository, either an url or a local path.
        tmp_dir (str): The path of the folder in which to clone the remote repository.

    Returns:
        Tuple[str,git.Repo]: The name of the repository and the repository object itself.

    """
    online_git_repo_regex = r"((git|ssh|http(s)?)|(git@[\w\.]+))(:(\/\/)?)" \
                            r"([\w\.@\:\-~\/]+\/)([\w\.@\:\-~]+)(\.git)?(\/)?"
    url_match = re.findall(online_git_repo_regex, repository_source)
    if url_match:
        # Remote git repository case
        repository_name = url_match[0][7]
        # print("Cloning repository")
        return repository_name, Repo.clone_from(repository_source, f"{tmp_dir}/{repository_name}", progress=Progress())
    else:
        # Local git repository case
        return repository_source.split("/")[-1], Repo(Path(repository_source))


class Progress(remote.RemoteProgress):
    global receiving_progress_bar
    global resolving_progress_bar
    receiving_progress_bar = tqdm(total=100, desc=f"Receiving data...", file=sys.stdout)
    resolving_progress_bar = tqdm(total=100, desc=f"Resolving data...", file=sys.stdout)

    def update(self, op_code, cur_count, max_count=None, message=''):
        global receiving_progress_bar
        global resolving_progress_bar
        if op_code == self.RECEIVING:
            receiving_progress_bar.update(int(100*cur_count/max_count) - receiving_progress_bar.n)
            receiving_progress_bar.refresh(nolock=True)
            if cur_count == max_count:
                del receiving_progress_bar

        if op_code == self.RESOLVING:
            resolving_progress_bar.update(int(100*cur_count/max_count) - resolving_progress_bar.n)
            resolving_progress_bar.refresh(nolock=True)
            if cur_count == max_count:
                del resolving_progress_bar

