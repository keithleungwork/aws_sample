"""Python program for LOCAL testing of estimator

Estimator is used to start a SageMaker Training task.
Before uploading the huge image to ECR and costing money on SageMaker Training,
we might want to ensure there is no bugs first.
That's why this local tester exists.

Possible issue:
    When I run into an issue with unfamiliar errors,
    I tried to increase the spec of Docker as below:
    - Memory: 8GB
    - Disk image size: 100GB
    And then the errors are gone, so if you saw some
    errors about memory allocation, try to set it as above.

"""
import argparse
import os
import sys
import logging
from dotenv import load_dotenv
from sagemaker.estimator import Estimator


# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.getLevelName("INFO"),
    handlers=[logging.StreamHandler(sys.stdout)],
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def main(args):
    """Main entry point
    Load the dataset file,
    convert into features and tokenize,
    train the model,
    save the model and tokenizer
    """

    # Set your AWS-CLI profile name here
    os.environ["AWS_PROFILE"] = args.profile_name
    logger.debug("Env AWS_PROFILE : ", os.environ["AWS_PROFILE"])

    target_image = args.local_image_name

    # These values will be passed to the train.py in container
    hyperparameters = {
        "dataset_filename": args.dataset_filename,
        # We just want to test locally, use a small value
        "batch_size": 1,
        "epochs": 1
    }

    estimator = Estimator(
        image_uri=target_image,
        role=args.aws_train_role,
        instance_count=1,
        hyperparameters=hyperparameters,
        instance_type='local'
    )

    # This will start a container and run the training,
    # with the train data source path set to channel "train"
    # i.e. inside the container, the env SM_CHANNEL_TRAIN will be set.
    estimator.fit({"train": args.train_data_path})

    logger.debug(estimator.model_data)


if __name__ == "__main__":
    # Load local env
    load_dotenv()
    # The default value are mostly from .env file
    # But still keep it as argument for flexibility
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile_name", type=str,
                        default=os.environ["AWS_PROFILE_NAME"])
    parser.add_argument("--dataset_filename", type=str,
                        default=os.environ["TRAIN_DATASET_FILENAME"])
    parser.add_argument("--local_image_name", type=str,
                        default=os.environ["TRAIN_LOCAL_IMAGE"])
    parser.add_argument("--train_data_path", type=str,
                        default=os.environ["TRAIN_DATA_PATH"])
    parser.add_argument("--aws_train_role", type=str,
                        default=os.environ["AWS_TRAIN_ROLE"])
    args, _ = parser.parse_known_args()

    logger.debug(f"profile_name: {args.profile_name}")
    logger.debug(f"dataset_filename: {args.dataset_filename}")
    logger.debug(f"local_image_name: {args.local_image_name}")
    logger.debug(f"train_data_path: {args.train_data_path}")
    logger.debug(f"aws_train_role: {args.aws_train_role}")

    main(args)
