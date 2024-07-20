from swagger_client import PrivateApi, PublicApi


class BaseHelper:
    def __init__(self, private_client=None, public_client=None):
        self.private_client: PrivateApi = private_client
        self.public_client: PublicApi = public_client
