import boto3
import json
import time
import os

def get_ai_review(code_diff: str) -> str:
    """
    Sends the code diff to Amazon Bedrock and gets an AI-powered review.
    
    Args:
        code_diff: The raw diff content from a Git pull request.
        
    Returns:
        A markdown-formatted string with the AI's code review and suggestions.
    """
    
    # Initialize the Bedrock runtime client
    bedrock_runtime = boto3.client(
        service_name='bedrock-runtime',
        region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    
    # The prompt to guide the AI for code review and suggestions
    prompt = f"""
    You are an expert software engineer and code reviewer. Your task is to analyze the following code diff for potential bugs, security vulnerabilities, performance issues, and best practices.

    For each issue you find, provide a brief, professional explanation and a corrected code block. If there are no issues, simply state "No significant issues found."

    Follow this exact format for each issue:

    ### Issue: [A concise, descriptive title]
    * [Explanation of the problem]
    * [Explanation of the corrected code]

    ```python
    # [Corrected code here, with comments]
    ```

    Here is the code diff to review:
    ```
    {code_diff}
    ```
    """
    
    # CORRECTED: Use the Messages API format for Claude 3 Sonnet
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4096,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ],
        "temperature": 0.2
    })
    
    # Corrected model ID for Claude 3 Sonnet
    model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'
    
    # Implement exponential backoff for API calls
    for i in range(5):
        try:
            response = bedrock_runtime.invoke_model(
                body=body,
                modelId=model_id,
                accept='application/json',
                contentType='application/json'
            )
            
            response_body = json.loads(response.get('body').read())
            # Handle the new Claude 3 response format
            return response_body['content'][0]['text']
        except Exception as e:
            print(f"Bedrock API call failed on attempt {i+1}. Retrying...")
            print(f"Error: {e}")
            time.sleep(2**i)
    
    return "Failed to get a response from the AI code reviewer."

