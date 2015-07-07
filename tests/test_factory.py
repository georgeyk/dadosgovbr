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

import types
import unittest

from dadosgovbr.factory import model_dict_factory, model_list_factory


class ModelItemsFactoryTestCase(unittest.TestCase):
    def test_empty(self):
        items = list(model_list_factory('test', []))
        self.assertEqual(items, [])

    def test_simple(self):
        item = list(model_list_factory('test', ['foo']))[0]
        self.assertEqual(item.__class__.__name__, 'Test')
        self.assertEqual(item.name, 'foo')

    def test_simple_with_field_name(self):
        item = list(model_list_factory('test', ['foo'], field_name='bar'))[0]
        self.assertTrue(hasattr(item, 'bar'))
        self.assertEqual(item.bar, 'foo')

    def test_simple_with_multiple_values(self):
        items = model_list_factory('test', range(10))
        for i, item in enumerate(items):
            self.assertEqual(item.name, i)

    def test_composed_class_name(self):
        item = list(model_list_factory('test bar', ['foo']))[0]
        self.assertEqual(item.__class__.__name__, 'TestBar')

        item = list(model_list_factory('test_bar', ['foo']))[0]
        self.assertEqual(item.__class__.__name__, 'Test_Bar')

    def test_with_nested_dict(self):
        item = list(model_list_factory('test', [{'foo': 'bar'}]))[0]
        self.assertEqual(item.__class__.__name__, 'Test')
        self.assertTrue(hasattr(item, 'foo'))
        self.assertEqual(item.foo, 'bar')

    def test_with_nested_list(self):
        item = list(model_list_factory('test', [['foo']]))[0]
        self.assertTrue(isinstance(item, types.GeneratorType))
        inner_item = list(item)[0]
        self.assertTrue(inner_item.__class__.__name__, 'Test')
        self.assertEqual(inner_item.name, 'foo')


class ModelDictFactoryTestCase(unittest.TestCase):

    def test_empty(self):
        item = model_dict_factory('test', {})
        self.assertEqual(item, None)

    def test_simple(self):
        item = model_dict_factory('test', {'foo': 'bar'})
        self.assertEqual(item.__class__.__name__, 'Test')
        self.assertTrue(hasattr(item, 'foo'))
        self.assertEqual(item.foo, 'bar')

    def test_simple_with_multiple_values(self):
        item = model_dict_factory('test', {'foo': 'bar', 'x': 1})
        self.assertTrue(hasattr(item, 'foo'))
        self.assertEqual(item.foo, 'bar')
        self.assertTrue(hasattr(item, 'x'))
        self.assertEqual(item.x, 1)

    def test_with_nested_list(self):
        item = model_dict_factory('test', {'foo': ['bar']})
        self.assertTrue(hasattr(item, 'foo'))
        self.assertTrue(isinstance(item.foo, types.GeneratorType))

        item_value = list(item.foo)[0]
        self.assertEqual(item_value.__class__.__name__, 'Foo')
        self.assertEqual(item_value.name, 'bar')

    def test_with_nested_dict(self):
        item = model_dict_factory('test', {'foo': {'aaa': 'bbb'}})
        self.assertTrue(hasattr(item, 'foo'))
        self.assertEqual(item.foo.__class__.__name__, 'Foo')
        self.assertTrue(hasattr(item.foo, 'aaa'))
        self.assertEqual(item.foo.aaa, 'bbb')


if __name__ == '__main__':
    unittest.main()
