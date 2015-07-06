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

from collections import namedtuple


def model_dict_factory(name, data):
    classname = ''.join([part.title() for part in name.split()])
    fields = ', '.join(data.keys())
    klass = namedtuple(classname, fields)
    if data:
        for key in data:
            if isinstance(data[key], list):
                data[key] = model_list_factory(key, data[key])
            if isinstance(data[key], dict):
                data[key] = model_dict_factory(key, data[key])
        return klass(**data)


def model_list_factory(name, items, field_name='name'):
    classname = ''.join([part.title() for part in name.split()])
    klass = namedtuple(classname, field_name)
    for item in items:
        if isinstance(item, dict):
            yield model_dict_factory(classname, item)
        elif isinstance(item, list):
            yield model_list_factory(classname, item)
        else:
            yield klass(item)
