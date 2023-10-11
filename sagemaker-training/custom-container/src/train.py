"""
The required arguments, setup, is from :
https://huggingface.co/docs/sagemaker/train#installation-and-setup
"""
import argparse
import os


def main(args):
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    ###########
    # Important arguments for sagemaker
    ###########
    # Assuming the input channel is "train"
    parser.add_argument("--data_path", type=str, default=os.getenv("SM_CHANNEL_TRAIN"))
    parser.add_argument("--model_output", type=str, default=os.getenv("SM_MODEL_DIR"))
    parser.add_argument("--other_output", type=str, default="/opt/ml/output/data")

    args, _ = parser.parse_known_args()
    for k, v in vars(args).items():
        print(f"{k}: {v}")

    main(args)
