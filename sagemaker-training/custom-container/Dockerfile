FROM python:3.11-slim


RUN apt-get update && apt-get install -y gcc wget vim less git poppler-utils && rm -rf /var/lib/apt/lists

# install the SageMaker Training Toolkit 
RUN pip3 install sagemaker-training

# install module dependencies
COPY requirements.txt /opt/
RUN pip install --upgrade pip && \
    pip install -r /opt/requirements.txt && \
    rm /opt/requirements.txt
# Reduce the image size
RUN pip cache purge

# Copy code to /opt/ml/code where training toolkit expects to find the script to run
# IMPORTANT !!!!! do not use `src/*`, otherwise the copy will not keep subfolder structure
COPY src/ /opt/ml/code/


# With training-toolkit package
# https://github.com/aws/sagemaker-training-toolkit#create-a-docker-image-and-train-a-model
# Defines train.py as script entry point
ENV SAGEMAKER_PROGRAM train.py
