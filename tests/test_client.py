# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

#
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

import os
import os.path
import unittest

import vcr

from dadosgovbr import DadosGovBR, DadosGovBRException

fixtures = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'fixtures')
json_vcr = vcr.VCR(serializer='json', cassette_library_dir=fixtures,
                   record_mode=os.environ.get('VCR_RECORD_MODE', 'once'))


class DadosGovBRClientTestCase(unittest.TestCase):
    def setUp(self):
        self.api = DadosGovBR()

    @json_vcr.use_cassette()
    def test_search_resources_simple(self):
        resources = list(self.api.search_resources('rouanet'))
        self.assertTrue(len(resources) > 0)
        for resource in resources:
            self.assertTrue('rouanet' in resource.name.lower())

    @json_vcr.use_cassette()
    def test_search_resources_with_param(self):
        resources = list(self.api.search_resources('civil', limit=2))
        self.assertEqual(len(resources), 2)

    @json_vcr.use_cassette()
    def test_search_resources_empty(self):
        resources = list(self.api.search_resources('arcoiro'))
        self.assertEqual(len(resources), 0)

    @json_vcr.use_cassette()
    def test_search_dataset_simple(self):
        datasets = list(self.api.search_datasets('supersimples'))
        self.assertEqual(len(datasets), 1)
        self.assertEqual(datasets[0].name, 'supersimples')

    @json_vcr.use_cassette()
    def test_search_dataset_empty(self):
        datasets = list(self.api.search_datasets('arcoiro'))
        self.assertEqual(len(datasets), 0)

    @json_vcr.use_cassette()
    def test_get_datasets(self):
        datasets = list(self.api.get_datasets())
        self.assertTrue(len(datasets) > 0)
        for dataset in datasets:
            self.assertTrue(hasattr(dataset, 'name'))

    @json_vcr.use_cassette()
    def test_get_dataset(self):
        dataset = self.api.get_dataset('cidadeshistoricas')
        self.assertEqual(dataset.name, 'cidadeshistoricas')
        self.assertTrue(hasattr(dataset, 'id'))

    @json_vcr.use_cassette()
    def test_get_dataset_by_id(self):
        dataset_id = '2c9bda21-f7db-4fd3-842a-0362873fb043'
        dataset = self.api.get_dataset(dataset_id)
        self.assertEqual(dataset.name, 'petroleo')
        self.assertEqual(dataset.id, dataset_id)

    @json_vcr.use_cassette()
    def test_get_dataset_not_found(self):
        with self.assertRaises(DadosGovBRException):
            self.api.get_dataset('arcoiro')

    @json_vcr.use_cassette()
    def test_get_tags(self):
        tags = list(self.api.get_tags())

        self.assertTrue(len(tags) > 0)
        for tag in tags:
            self.assertTrue(hasattr(tag, 'name'))

    @json_vcr.use_cassette()
    def test_get_tag(self):
        tag = self.api.get_tag('vestibular')
        self.assertEqual(tag.name, 'vestibular')
        self.assertTrue(hasattr(tag, 'id'))

    @json_vcr.use_cassette()
    def test_get_tag_by_id(self):
        tag_id = '35018a82-1981-4b68-9c4f-57689169f9a7'
        tag = self.api.get_tag(tag_id)
        self.assertEqual(tag.name, 'universidades')
        self.assertEqual(tag.id, tag_id)

    @json_vcr.use_cassette()
    def test_get_tag_not_found(self):
        with self.assertRaises(DadosGovBRException):
            self.api.get_tag('arcoiro')


if __name__ == '__main__':
    unittest.main()
