import argparse
import datetime
import logging.config
from pathlib import Path

import yaml

import src.aws_utils as aws

 # Upload all artifacts to S3
logging.config.fileConfig("config/logging/local.conf")
logger = logging.getLogger("clouds")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Acquire, clean, and create features from clouds data"
    )
    parser.add_argument(
        "--config", default="config/config.yaml", help="Path to configuration file"
    )
    args = parser.parse_args()

    # Load configuration file for parameters and run config
    with open(args.config, "r") as f:
        try:
            config = yaml.load(f, Loader=yaml.FullLoader)
        except yaml.error.YAMLError as e:
            logger.error("Error while loading configuration from %s", args.config)
        else:
            logger.info("Configuration file loaded from %s", args.config)

    run_config = config.get("run_config", {})
 

aws_config = config.get("aws")
if aws_config["upload"] is True:
    aws.upload_flight(aws_config)