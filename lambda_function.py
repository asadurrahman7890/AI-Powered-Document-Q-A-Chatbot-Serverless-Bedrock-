# lambda_function.py
import os
import json
import boto3
from botocore.exceptions import ClientError

REGION = os.environ.get("AWS_REGION", "us-east-1")
BUCKET = os.environ["BUCKET"]       # e.g., 'your-bucket-name'
KEY = os.environ["KEY"]             # e.g., 'policy.txt' or 'data.csv'
MODEL_ID = os.environ["MODEL_ID"]   # e.g., 'us.deepseek.r1-v1:0' or your model ID

s3 = boto3.client("s3", region_name=REGION)
bedrock = boto3.client("bedrock-runtime", region_name=REGION)

def read_document_from_s3(bucket, key):
    obj = s3.get_object(Bucket=bucket, Key=key)
    body = obj["Body"].read()
    try:
        text = body.decode("utf-8")
    except Exception:
        text = str(body)
    return text

def call_deepseek(prompt, max_tokens=512, temperature=0.0):
    payload = {"inputText": prompt, "maxTokens": max_tokens, "temperature": temperature}
    # Some models accept 'inputText'; if your model requires another format, adjust here.
    resp = bedrock.invoke_model(
        modelId=MODEL_ID,
        contentType="application/json",
        body=json.dumps(payload)
    )
    resp_body = resp["body"].read().decode("utf-8")
    try:
        j = json.loads(resp_body)
    except Exception:
        # If response is plain text, return it
        return resp_body

    # Try a few common response fields
    if "outputText" in j:
        return j["outputText"]
    if "choices" in j and isinstance(j["choices"], list) and len(j["choices"])>0:
        # some models return {"choices":[{"text":"..."}]}
        c = j["choices"][0]
        return c.get("text") or c.get("message") or c.get("delta") or json.dumps(c)
    # fallback: return whole JSON
    return json.dumps(j)

def lambda_handler(event, context):
    try:
        # event from API Gateway: body is JSON string
        incoming = event.get("body")
        if incoming:
            body = json.loads(incoming)
        else:
            body = event

        question = body.get("query") or body.get("question") or ""
        if not question:
            return {"statusCode":400, "body": json.dumps({"error":"Missing field 'query' in request body."})}

        # Read document from S3 (small file recommended for free tier)
        document_text = read_document_from_s3(BUCKET, KEY)

        prompt = (
            "You are an assistant that answers user questions only from the provided document. "
            "Do not invent facts. If answer not in document, say 'Not in document'.\n\n"
            f"Document:\n{document_text}\n\nQuestion: {question}\nAnswer:"
        )

        answer = call_deepseek(prompt, max_tokens=256, temperature=0.0)

        return {"statusCode":200, "body": json.dumps({"answer": answer})}

    except ClientError as e:
        return {"statusCode":500, "body": json.dumps({"error":"AWS error","details":str(e)})}
    except Exception as e:
        return {"statusCode":500, "body": json.dumps({"error":"Internal error","details":str(e)})}
