import os

from dotenv import load_dotenv
# from sagemaker.workflow.pipeline_context import LocalPipelineSession
from sagemaker.local import LocalSession
from sagemaker.processing import Processor, ProcessingInput, ProcessingOutput

# Keep on top to load from .env file
load_dotenv()

# local mode https://sagemaker.readthedocs.io/en/stable/overview.html#local-mode
sagemaker_session = LocalSession()
sagemaker_session.config = {'local': {'local_code': True}}

# https://sagemaker.readthedocs.io/en/stable/api/training/processing.html#sagemaker.processing.ScriptProcessor
script_eval = Processor(
    image_uri=os.getenv("LOCAL_IMAGE_NAME"),
    instance_count=1,
    role=os.getenv("AWS_ROLE"),
    sagemaker_session=sagemaker_session,
    entrypoint=["python3", "src/main.py"],
)


# https://sagemaker.readthedocs.io/en/stable/api/training/processing.html#sagemaker.processing.ScriptProcessor
container_input_path = "/opt/ml/processing/input_data/"
container_output_path = "/opt/ml/processing/evaluation/"
_ = script_eval.run(
    arguments=[
        "--some_args", "somevalues",
    ],
    inputs=[
        ProcessingInput(
            source="S3 path here",
            destination=container_input_path,
        )
    ],
    # https://sagemaker.readthedocs.io/en/stable/api/training/processing.html#sagemaker.processing.ProcessingOutput
    outputs=[
        ProcessingOutput(
            output_name="evaluation",
            source=container_output_path,
            destination="S3 path here",
        ),
    ],
    wait=True,
    logs=True,
)
