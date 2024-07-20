from support.helpers.api.base_api_helper import BaseHelper


class ObjectHelper(BaseHelper):
    def __init__(self, private_client=None, public_client=None):
        super().__init__(private_client=private_client, public_client=public_client)

    def get_object(self, object_id: str, options='{"infoLevel":"full"}'):
        return self.private_client.database_object_get(object_id=object_id, options=options).get('data')
