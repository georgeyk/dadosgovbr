# dadosgovbr

[![PyPI version](https://badge.fury.io/py/dadosgovbr.svg)](http://badge.fury.io/py/dadosgovbr)
[![Build Status](https://travis-ci.org/georgeyk/dadosgovbr.svg?branch=master)](https://travis-ci.org/georgeyk/dadosgovbr)
[![Coverage Status](https://coveralls.io/repos/georgeyk/dadosgovbr/badge.svg?branch=master)](https://coveralls.io/r/georgeyk/dadosgovbr?branch=master)


---

A library to programatically explore the Brazilian open data program.

More details at [dados.gov.br][1]

## Motivation

Basically, I did this library because their web interface was broken for me, specially the search feature.

Also, I feel more confortable exploring the data using a python shell with all the libraries available to handle json,
csv and so on.


## Examples

The library just provides a "object-wrapping" from the results of the API, so we can access every attribute as we
inspect any regular python object:

```python

>>> from dadosgovbr DadosGovBR
>>> api = DadosGovBR()
>>> api.get_tag('VT')
Tag(vocabulary_id=None, packages=<generator object model_list_factory at 0x7f7dac17af00>, display_name=u'VT',
id=u'41a7ab78-3cec-44a3-b2c3-ca15ad55a50f', name=u'VT')
```

Check the tests directory for more examples, like [this one][tests/example.py].


## NOTE

This is very *work-in-progress* lib.
Contributions are super-welcome. =)


[1]: http://dados.gov.br/dataset
