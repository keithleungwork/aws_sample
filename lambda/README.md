# AWS Lambda Template

This template is a quickstart to integrate code into lambda

## Setup

Please make changes in following session accordingly.

### .env file
Copy .env.sample to create .env file.
This env file is loaded when locally testing lambda so we can override AWS credential if any traffic needed to access AWS.


### Dockerfile

This template copy the code located in `./src` in lambda image. Please modify it to include other files if necessary.


-----

## Local Execution

A basic makefile is provided, you can run
- `make build` can build the lambda image locally
- `make run` can start the lambda function locally for testing.


Then, use your favorite API testing tool to invoke the endpoint as below
 - Local API : http://localhost:9000/2015-03-31/functions/function/invocations
 - Method: GET
 - Request Payload:
     ```json
      {

      }
     ```