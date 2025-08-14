# main.py
import os
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from bedrock_client import get_ai_review
from github_client import post_pr_comment, get_pr_diff

app = FastAPI()

class Payload(BaseModel):
    repository: str
    pull_request_number: int
    diff: str = "" # We no longer need to pass the diff, but keep it for validation

@app.post("/review")
async def review_code(payload: Payload):
    """
    Receives a webhook payload with PR details, gets the diff from GitHub,
    gets an AI review, and posts a comment.
    """
    print(f"Received request for PR #{payload.pull_request_number} on {payload.repository}")
    
    # NEW: Fetch the diff directly from the GitHub API
    diff = get_pr_diff(payload.repository, payload.pull_request_number)
    if not diff:
        return {"status": "error", "message": "Failed to get PR diff from GitHub."}
    
    # Get AI review and code suggestions from Amazon Bedrock
    review_comment = get_ai_review(diff)
    
    # Post the comment to the GitHub pull request
    success = post_pr_comment(
        repo_name=payload.repository,
        pr_number=payload.pull_request_number,
        comment=review_comment
    )
    
    if success:
        return {"status": "success", "message": "Code review posted to PR."}
    else:
        return {"status": "error", "message": "Failed to post code review."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
