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



from __future__ import print_function, unicode_literals
import csv

import requests

from dadosgovbr import DadosGovBR


# Usage example of DadosGovBR library:

api = DadosGovBR()

resources = list(api.search_resources(u'cidades históricas'))
print('Found {} results for "{}" query'.format(len(resources), u'cidades históricas'))

# Let's see if we find csv format resource:

for resource in resources:
    if resource.format == 'CSV':
        print('CSV Resource:')
        print('- {} - ID: {}'.format(resource.name, resource.id))
        print('- {}'.format(resource.url))
        print('{} CSV Content {}'.format('-' * 10, '-' * 10))
        data = [row for row in csv.reader(requests.get(resource.url).content.splitlines())]
        print('Fieldnames: {}'.format(data[0]))
        print('First line content: {}'.format(data[1]))
        break
