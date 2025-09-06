# AI-Powered-Document-Q-A-Chatbot-Serverless-Bedrock-
eploying it on AWS (S3 → Lambda → Bedrock → API Gateway), step-by-step and beginner-friendly. I’ll include exact commands, the Lambda code to paste, how to test, and cleanup tips.

Follow the steps in order; I’ve added links to the official docs at the key points so you can click for more detail.

1) What we’ll do (high level)

Prepare a local repo with the project files (lambda_function.py, README.md, policy.txt/policy.csv, architecture.png).

Create a GitHub repo and push your project.

Upload your policy.txt (or CSV) to S3.

Create an IAM role for Lambda (S3 read + Bedrock invoke + lambda logging).

Create the Lambda function, set env vars, upload code.

Create an API Gateway HTTP API and connect it to Lambda.

Test end-to-end with curl.

Monitor logs and clean up when finished.
2) Prepare project files locally

Create a folder called chatbot-bedrock-qna and inside create these files.

a. lambda_function.py — paste this (robust and beginner-friendly):
policy.txt (or policy.csv) — add the text you want the bot to read. If you already uploaded a CSV, the Lambda will read it as raw text (that works for simple testing).

d. architecture.png — save the small architecture image in repo (or create a simple diagram).
