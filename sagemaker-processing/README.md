# Sagemaker Processing template


# How to Use

- Sagemaker processing is easier to integrate than training. You can build a very general docker image. Just make sure your script read files input from and write output to a set of configurable paths.
- To start, put your scripts into `./src`, and modify Dockerfile ENTRYPOINT to point to the main script.



# Sagemaker Processing Local Testing

To execute local mode, follow below step:
1. Copy `.env.sample` to create `.env` and fill in those ENV variable. You need S3 bucket source and destination path for testing. (Or You can modify the local script to use local files)
2. Build the image locally.
3. Now you can execute local script by `python3 local_sagemaker.py`. Note that you need to configure AWS auth properly if not on sagemaker notebook.