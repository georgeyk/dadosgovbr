# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

# The MIT License (MIT)
# Copyright (C) 2015 - George Y. Kussumoto <contato@georgeyk.com.br>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

# Not an extensive implementation, more information at:
# http://docs.ckan.org/en/ckan-2.2.2/api.html#get-able-api-functions

from __future__ import unicode_literals
import logging

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

import requests

from .factory import model_dict_factory, model_items_factory


logger = logging.getLogger(__name__)


class DadosGovBRException(Exception):
    pass


class DadosGovBR(object):
    base_api_url = 'http://dados.gov.br/api'
    api_version = 3
    endpoint = '{}/{}/action'.format(base_api_url, api_version)
    timeout = 4

    def _request(self, resource, **params):
        url = '{endpoint}/{resource}?{params}'.format(
            endpoint=self.endpoint, resource=resource, params=urlencode(params))
        logger.info('Request URL: {}'.format(url))

        response = requests.get(url, timeout=self.timeout)
        logger.info('Response: status {}'.format(response.status_code))

        data = response.json()
        if data['success']:
            return data['result']
        else:
            logger.debug('Response error: headers={}, content={}, '.format(response.headers, response.content))
            raise DadosGovBRException(data['error'])

    #
    # Public API
    #

    def search_resources(self, query, search_key='name', **kwargs):
        query = '{}:{}'.format(search_key, query)
        result = self._request('resource_search', query=query, **kwargs)
        for resource in result['results']:
            yield model_dict_factory('resource', resource)

    def search_dataset(self, query, **kwargs):
        result = self._request('package_search', q=query, **kwargs)
        for dataset in result['results']:
            yield model_dict_factory('dataset', dataset)

    def get_datasets(self):
        return model_items_factory('dataset item', self._request('package_list'))

    def get_dataset(self, dataset_id):
        dataset = self._request('package_show', id=dataset_id)
        return model_dict_factory('dataset', dataset)

    def get_tags(self):
        tags = self._request('tag_list')
        return model_items_factory('tag item', tags)

    def get_tag(self, tag_id):
        tag = self._request('tag_show', id=tag_id)
        return model_dict_factory('tag', tag)
