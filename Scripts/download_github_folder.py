import os
import requests

def download_github_subfolder(repo: str, folder_path: str, branch: str = "main") -> None:
    """Download a specific subfolder from a GitHub repo into the current directory."""
    api_url = f"https://api.github.com/repos/{repo}/contents/{folder_path}?ref={branch}"
    response = requests.get(api_url)

    if response.status_code != 200:
        raise RuntimeError(f"GitHub API error: {response.status_code} - {response.text}")

    items = response.json()

    for item in items:
        name = item["name"]
        path = item["path"]
        item_type = item["type"]

        if item_type == "file":
            download_url = item["download_url"]
            local_path = os.path.join(".", path.split("/", 1)[1] if "/" in path else path)
            local_dir = os.path.dirname(local_path)

            if not os.path.exists(local_dir):
                os.makedirs(local_dir, exist_ok=True)

            file_data = requests.get(download_url)
            with open(local_path, "wb") as f:
                f.write(file_data.content)

        elif item_type == "dir":
            download_github_subfolder(repo, path, branch)

    return None


if __name__ == "__main__":

    download_github_subfolder(
        repo="rohan-gt/deeplearning-ai-courses",
        folder_path="Courses/Machine Learning/00. Prerequisites",
        branch="main"
    )
