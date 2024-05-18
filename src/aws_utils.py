import logging.config
import sys
from pathlib import Path

import boto3
import botocore

logging.config.fileConfig("config/logging/local.conf")
logger = logging.getLogger("clouds")

def upload_flight(config):
    """Upload all the artifacts in the specified directory to S3.

    Args:
        artifacts: Directory containing all the artifacts from a given experiment.
        config: Config required to upload artifacts to S3; see example config file for structure.

    Returns:
        List of S3 URIs for each file that was uploaded.
    """

    logger.info("Uploading the data to S3.")

    try:
        # Initialize S3 client
        session = boto3.Session()
        s3_client = session.client("s3")
    except botocore.exceptions.ClientError as e:
        logger.error("Failed to initialize S3 client: %s", e)
        sys.exit(1)

    # except botocore.exceptions.InvalidConfigError:
    #     logger.critical("Invalid configuration. Please check your AWS config details.")
    #     sys.exit(1)

    # List of uploaded file paths
    uploaded_files = []
    bucket_name = config["bucket_name"]

    # Check if the bucket exists and create if it doesn't
    logger.info("Check if the bucket exists and create if it doesn't.")
    s3_client.head_bucket(Bucket=bucket_name)
    
    try:
        # Iterate over files in the directory
        artifacts_path = Path('data/')
        for file_path in artifacts_path.glob("*"):
            if file_path.is_file():
                # Construct S3 key (object key)
                s3_key = str(file_path.name)

                # Upload file to S3
                print(f"Upload the data {s3_key} to s3.")
                s3_client.upload_file(Filename=str(file_path), Bucket=bucket_name, Key=s3_key)

                # Append S3 URI to the list
                uploaded_files.append(f"s3://{bucket_name}/{s3_key}")

        logger.info("Upload successful to s3.")
        return uploaded_files

    except botocore.exceptions.ClientError as e:
        logger.error("Failed to upload artifacts to S3: %s", e)
        sys.exit(1)
