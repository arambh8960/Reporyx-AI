import os
import shutil
from git import Repo


def extract_repo_name(repo_url: str) -> str:
    return repo_url.rstrip("/").split("/")[-1]


def clone_repository(repo_url: str):
    repo_name = extract_repo_name(repo_url)

    base_dir = "repositories"
    os.makedirs(base_dir, exist_ok=True)

    repo_path = os.path.join(base_dir, repo_name)

    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)

    Repo.clone_from(repo_url, repo_path)

    return {
        "repo_name": repo_name,
        "repo_path": repo_path
    }