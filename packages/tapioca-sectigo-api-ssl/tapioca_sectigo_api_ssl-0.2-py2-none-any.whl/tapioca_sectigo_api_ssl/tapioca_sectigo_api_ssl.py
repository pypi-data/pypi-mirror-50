# coding: utf-8
from requests.auth import HTTPBasicAuth
from tapioca import (
    TapiocaAdapter, generate_wrapper_from_adapter, JSONAdapterMixin)


from .resource_mapping import RESOURCE_MAPPING


class Sectigo_api_sslClientAdapter(JSONAdapterMixin, TapiocaAdapter):
    api_root = 'https://secure.comodo.com'
    resource_mapping = RESOURCE_MAPPING

    def get_request_kwargs(self, api_params, *args, **kwargs):
        params = super(Sectigo_api_sslClientAdapter, self).get_request_kwargs(
            api_params, *args, **kwargs)

        params['auth'] = HTTPBasicAuth(
            api_params.get('loginName'), api_params.get('loginPassword'))

        return params

    def get_iterator_list(self, response_data):
        return response_data

    def get_iterator_next_request_kwargs(self, iterator_request_kwargs,
                                         response_data, response):
        pass


Sectigo_api_ssl = generate_wrapper_from_adapter(Sectigo_api_sslClientAdapter)
