from support.clients.aws_client import AWSClient


class MinioClient:
    def __init__(self, endpoint, access_key, secret_key):
        self.client = AWSClient(endpoint=endpoint, access_key=access_key, secret_key=secret_key)
