# https://docs.aws.amazon.com/sagemaker/latest/dg/build-your-own-processing-container.html
FROM python:3.11-slim

# Copy the requirements file and install the dependencies then clear the cache
COPY requirements.txt /tmp/
RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt && \
    rm -rf /root/.cache

# Copy source code
COPY . /opt/code/
WORKDIR /opt/code/
ENTRYPOINT ["python3", "src/main.py"]
