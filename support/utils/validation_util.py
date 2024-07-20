class Validator:
    def __init__(self, response, data=None):
        if isinstance(response, str):
            self.response = {'data': response}
        else:
            self.response = response
            if 'status' in response:
                self.response_status = response['status']

        if data is not None:
            self.response = self.response[data]

    def validate_status(self, expected_status):
        assert self.response_status == expected_status, f'API response status should be {expected_status}'
        return self

    def validate_schema(self, schema):
        schema.model_validate(self.response)
