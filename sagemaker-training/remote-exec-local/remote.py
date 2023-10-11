from sagemaker.remote_function import remote

from libs.helper import plus_one


@remote(instance_type="ml.m5.xlarge", dependencies='./requirements.txt', include_local_workdir=True)
def main(x, y):
    return plus_one(x), plus_one(plus_one(y))


output = main(1, 10)
print(output)
