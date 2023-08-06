# coding: utf-8

from tapioca import (
    TapiocaAdapter, generate_wrapper_from_adapter, JSONAdapterMixin)


from .resource_mapping import RESOURCE_MAPPING


class SuperlogicaClientAdapter(JSONAdapterMixin, TapiocaAdapter):
    api_root = 'https://api.superlogica.net/v2/'
    resource_mapping = RESOURCE_MAPPING

    def get_request_kwargs(self, api_params, *args, **kwargs):
        params = super(SuperlogicaClientAdapter, self).get_request_kwargs(
            api_params, *args, **kwargs)

        params['headers'].update(api_params)

        return params

    def get_iterator_list(self, response_data):
        return response_data

    def get_iterator_next_request_kwargs(self, iterator_request_kwargs,
                                         response_data, response):
        pass


Superlogica = generate_wrapper_from_adapter(SuperlogicaClientAdapter)
