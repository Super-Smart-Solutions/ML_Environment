import boto3
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize the S3 client with credentials from environment variables
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_DEFAULT_REGION')
)


# Try listing buckets to check credentials
response = s3_client.list_buckets()
print(response)
