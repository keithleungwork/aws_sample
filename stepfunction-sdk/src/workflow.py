# Ref: https://github.com/aws/amazon-sagemaker-examples/blob/main/step-functions-data-science-sdk/step_functions_mlworkflow_processing/step_functions_mlworkflow_scikit_learn_data_processing_and_model_evaluation.ipynb
import re
import textwrap
import logging
import uuid

from stepfunctions.steps import Chain, ProcessingStep, TrainingStep
from stepfunctions.workflow import Workflow
from stepfunctions.steps.states import Fail, Catch
from sagemaker import TrainingInput
from sagemaker.processing import Processor, ProcessingInput, ProcessingOutput
from sagemaker.estimator import Estimator


# Set up logging
handler = logging.StreamHandler()
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def sm_job_name_builder(job_name: str) -> str:
    # Only hyphen is allowed in job name, max length is 63
    # Ref: https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_CreateTrainingJob.html
    filtered = re.sub(r"[^\-a-zA-Z0-9]", "", job_name)
    # Without hyphen to reduce length
    filtered += "-" + uuid.uuid4().hex
    # Truncate the job name to be less than (63 - UUID length) chars
    # Because UUID is used in job name suffix
    return textwrap.shorten(filtered, 63, placeholder="")


def get_process_step(steps_params: dict, workflow_config: dict):
    step_key = "processing"
    cfg = workflow_config["steps"][step_key]

    sm_processor = Processor(
        image_uri=cfg["image_uri"],
        role=cfg["role"],
        instance_count=cfg["instance_count"],
        instance_type=cfg["instance_type"],
        volume_size_in_gb=cfg["volume_size_in_gb"],
        max_runtime_in_seconds=cfg["max_runtime_in_seconds"],
        # This refers to the entrypoint in component
        entrypoint=["python3", "src/some_script.py"],
    )

    return ProcessingStep(
        step_key,
        processor=sm_processor,
        job_name=sm_job_name_builder("some_processing"),
        inputs=[ProcessingInput(
            source="s3://somewhere/inputs/",
            destination="/opt/ml/processing/input_data/",
            input_name="dataset"
        )],
        outputs=[ProcessingOutput(
            source="/opt/ml/processing/some_output/",
            destination="s3://somewhere/outputs/",
            output_name="result",
        )],
        container_arguments=steps_params["some_processing"].get("container_arguments", None),
    )


def get_train_step(steps_params: dict, workflow_config: dict):
    step_key = "training"
    cfg = workflow_config["steps"][step_key]

    estimator = Estimator(
        image_uri=cfg["image_uri"],
        role=cfg["role"],
        instance_count=cfg["instance_count"],
        instance_type=cfg["instance_type"],
        volume_size=cfg["volume_size"],
        max_run=cfg["max_run"],
        # Important to set this to False, otherwise the output will be compressed in 1 large file
        disable_output_compression=True,
    )
    return TrainingStep(
        step_key,
        estimator=estimator,
        # Wrap the s3 path with TrainingInput
        data={k: TrainingInput(v) for k, v in steps_params["input"].items()},
        output_data_config_path=steps_params["output"],
        # These values will be passed to the train.py as arguments in container
        hyperparameters=steps_params["some_training"].get("hyperparameters", None),
        job_name=sm_job_name_builder("some_training"),
        # wait for the training job to complete before proceeding to the next step
        wait_for_completion=True,
    )


def create_chain(steps_params: dict, workflow_config: dict) -> Chain:
    """Create a chain of execution steps.

    Args:
        steps_params (dict): parameters for each step
        workflow_config (dict): workflow config

    Returns:
        Chain: Chain of execution steps
    """
    # Init a list to store states
    chain_ls = []
    # Create training step
    train_step = get_train_step(steps_params, workflow_config)
    chain_ls.append(train_step)
    # Create processing step
    process_step = get_process_step(steps_params, workflow_config)
    chain_ls.append(process_step)

    # =======================================
    # Add the global Error handling in the workflow
    # Create Fail state to mark the workflow failed in case any of the steps fail.
    failed_state = Fail("ML Workflow failed", cause="Workflow failed")
    # We will use the Catch Block to perform error handling.
    # If the Processing Job Step or Training Step fails, the flow will go into failure state.
    catch_state = Catch(
        error_equals=["States.TaskFailed"],
        next_step=failed_state,
    )
    # Add catch to all states
    for state in chain_ls:
        state.add_catch(catch_state)
    return Chain(chain_ls)


def get_workflow(workflow_execution_role: str, workflow_arn: str, workflow_graph: Chain) -> Workflow:
    """Given a workflow execution role, workflow arn and workflow graph, attach and update the workflow.
    Then return the workflow instance.

    Args:
        workflow_execution_role (str): exec role
        workflow_arn (str): target SFN arn
        workflow_graph (Chain): Chain instance

    Returns:
        Workflow: workflow instance
    """
    # Attach the existing workflow to the instance
    workflow_inst = Workflow.attach(workflow_arn)
    # Update SFN definition and role
    workflow_inst.update(workflow_graph, role=workflow_execution_role)
    logger.info("Workflow updated with new definition/role")
    return workflow_inst


# def exec_updated_workflow(workflow_params: dict, steps_params: dict, workflow_config: dict):
def exec_updated_workflow(lambda_input: dict, workflow_config: dict):
    workflow_execution_role = workflow_config["workflow"]["role"]
    workflow_arn = workflow_config["workflow"]["arn"]

    # Create the chain of execution steps, by passing the ExecutionInput placeholder
    workflow_graph = create_chain(lambda_input, workflow_config)
    # Attach and update workflow
    workflow_inst = get_workflow(workflow_execution_role, workflow_arn, workflow_graph)

    # Execute workflow
    logger.info("Executing workflow ARN: {}".format(workflow_arn))
    execution = workflow_inst.execute(inputs={"comment": "Triggered from Lambda"})
    logger.info("Execution started with ARN: {}".format(execution.execution_arn))
