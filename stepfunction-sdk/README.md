# StepFunction SDK Template

This template allows you to quickly startup a workflow builder.
For demonstration, the workflow contains 2 steps
- SageMaker Training Task
- SageMaker Processing Task


## Prerequisite

- Assuming each steps executes with own docker images, these images should be ALREADY pushed to ECR. Their ARN is needed in coding this workflow.
- This workflow builder does NOT create but atttach & update an existing one. So create a StepFunction manually first, and get the ARN ready.
  - The reason is, creating and updating together rely only on the workflow "name" to match, that can be risky.
  - Instead, attaching & updating rely on ARN, that cannot be wrong.
- ARN of each execution roles IAM for the workflow, each steps are necessary.


## Advice: Lambda Function

The stepfunction sdk itself is very helpful, but StepFunction + SageMaker intergration can be tricky, for example when dealing with I/O path, dynamic job name...etc

As a workaround, I recommend you to use Lambda Function for updating & executing SFN.
So that you have a full control on how each steps take the I/O, configuration without the need to fine-tune the path and bugs.
The downside is, with the lambda function handling all I/O and invoking, it becomes not appropriate to start an execution of SFN directly without the Lambda.
