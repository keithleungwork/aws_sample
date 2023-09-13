# Use an image from https://github.com/aws/deep-learning-containers/blob/master/available_images.md
FROM 


RUN apt-get update && apt-get install -y gcc wget vim less git poppler-utils && rm -rf /var/lib/apt/lists

COPY requirements.txt /opt/
RUN pip install --upgrade pip
RUN pip install -r /opt/requirements.txt && rm /opt/requirements.txt
# Reduce the image size
RUN pip cache purge

# Copy code to /opt/ml/code where sagemaker-containers expects to find the script to run
COPY src/* /opt/ml/code/

# With sagemaker-training package
# https://github.com/aws/sagemaker-training-toolkit/tree/53a9a0527a46df62eca86f98456e0e53fd9e90fe
# Defines train.py as script entry point
ENV SAGEMAKER_PROGRAM train.py

# if without sagemaker-training package
# https://docs.aws.amazon.com/sagemaker/latest/dg/your-algorithms-training-algo-dockerfile.html
# WORKDIR /opt/ml/code/
# ENTRYPOINT [ "python", "train.py" ]
