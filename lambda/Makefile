IMAGE_NAME=lambda_template

# Build lambda image
build:
	docker build -t $(IMAGE_NAME):latest -f ./Dockerfile .

# Run Lambda function locally for testing
run:
	docker run --rm --name $(IMAGE_NAME)  -p 9000:8080 -v ${PWD}/tmp:/tmp --env-file .env $(IMAGE_NAME):latest