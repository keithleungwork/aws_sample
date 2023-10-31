from pathlib import Path
import yaml

from workflow import exec_updated_workflow


# Using lambda function is recommended, refer to README
def lambda_handler(event, _):
    # Config (from yaml)
    if event["config"] == "development":
        config_path = Path(__file__).parent / "development.yml"
    else:
        raise ValueError("Invalid config name: {}".format(event["config"]))
    with open(config_path, "rb") as f:
        workflow_config = yaml.load(f.read(), Loader=yaml.SafeLoader)
    # Execute workflow
    exec_updated_workflow(event, workflow_config)


if __name__ == "__main__":
    # Param (from arguments of lambda)
    lambda_input = {
        "config": "development",
        "input": {
            "image": "s3://somewhere/some_images/",
            "label": "s3://somewhere/some_xmls/"
        },
        "output": "s3://somewhere/some_outputs/",
        "some_training": {
            "hyperparameters": {
                "any_params": "anything"
            }
        },
        "some_processing": {
            "container_arguments": [
                "--some_path", "some_value"
            ]
        }
    }
    res = lambda_handler(lambda_input, None)

    print(res)
