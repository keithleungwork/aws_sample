FROM python:3.11-slim


RUN apt-get update && apt-get install -y gcc wget vim less git curl && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Packages installation
COPY requirements.txt /opt/
RUN pip install --upgrade pip && \
    pip install awslambdaric && \
    pip install -r /opt/requirements.txt && \
    rm /opt/requirements.txt && \
    rm -rf /root/.cache

# Install RIE
RUN curl -Lo /usr/local/bin/aws-lambda-rie \
    https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie \
    && chmod 755 /usr/local/bin/aws-lambda-rie


# For choosing between local test(RIE) or run with real lambda (RIC)
COPY entry_script.sh /

# Copy core code
WORKDIR /function
# IMPORTANT !!!!! do not use `src/*`, otherwise the copy will not keep subfolder structure
COPY src/ /function/

ENTRYPOINT [ "/entry_script.sh" ]
CMD [ "app.lambda_handler" ]