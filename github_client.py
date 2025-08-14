# github_client.py
import requests
import os

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_API_URL = "https://api.github.com"

def get_pr_diff(repo_name: str, pr_number: int) -> str:
    """
    Fetches the code diff for a specific GitHub Pull Request.
    
    Args:
        repo_name: The name of the GitHub repository (e.g., 'owner/repo').
        pr_number: The number of the pull request.
        
    Returns:
        The raw diff content as a string, or an empty string on failure.
    """
    if not GITHUB_TOKEN:
        print("Error: GITHUB_TOKEN environment variable not set.")
        return ""
    
    url = f"{GITHUB_API_URL}/repos/{repo_name}/pulls/{pr_number}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.diff"  # Corrected header
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Failed to get PR diff for PR #{pr_number}: {e}")
        return ""

def post_pr_comment(repo_name: str, pr_number: int, comment: str) -> bool:
    """
    Posts a comment to a specific GitHub Pull Request.
    """
    if not GITHUB_TOKEN:
        print("Error: GITHUB_TOKEN environment variable not set.")
        return False
    
    url = f"{GITHUB_API_URL}/repos/{repo_name}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "body": comment
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        print(f"Successfully posted comment to PR #{pr_number}.")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Failed to post comment to PR #{pr_number}: {e}")
        return False

