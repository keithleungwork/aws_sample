#!/bin/sh
# ref:  https://docs.aws.amazon.com/lambda/latest/dg/images-test.html#images-test-alternative
if [ -z "${AWS_LAMBDA_RUNTIME_API}" ]; then
  # Local test
  exec /usr/local/bin/aws-lambda-rie /usr/local/bin/python -m awslambdaric $@
else
  # real Lambda runtime
  exec /usr/local/bin/python -m awslambdaric $@
fi