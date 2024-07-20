from support.builders.search_query_builder import SearchQueryBuilder
from support.helpers.api.base_api_helper import BaseHelper
from support.helpers.wait_helper import wait_for
from swagger_client import CreateSearchRequest


def wait_until_search_finished_condition(search_data):
    return search_data is not None and search_data['isComplete']


def search_data_with_wait(search_data_method):
    return wait_for(search_data_method, wait_until_search_finished_condition)


class SearchHelper(BaseHelper):
    def __init__(self, private_client=None, public_client=None):
        super().__init__(private_client=private_client, public_client=public_client)

    def search(self, object_name, *conditions):
        search_builder = SearchQueryBuilder(object_name=object_name)
        for condition in conditions:
            search_builder = search_builder.where(condition)
        search_query = search_builder.build()
        create_search_request: CreateSearchRequest = CreateSearchRequest(select=search_query)
        create_search_response = self.private_client.database_search_post(
            create_search_body=create_search_request)
        return search_data_with_wait(lambda: self.search_data(create_search_response))

    def search_data(self, create_search_response=None):
        create_search_results = self.private_client \
            .database_search_get(search_id=create_search_response['data'])
        return create_search_results['data']