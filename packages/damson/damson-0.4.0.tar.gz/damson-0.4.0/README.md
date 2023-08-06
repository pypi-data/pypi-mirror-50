Damson: A Concise Python Validation Library™
==========================

[![image](https://img.shields.io/pypi/v/damson.svg)](https://pypi.org/project/damson/)
[![image](https://img.shields.io/pypi/l/damson.svg)](https://pypi.org/project/damson/)
[![image](https://img.shields.io/pypi/pyversions/damson.svg)](https://pypi.org/project/requests/)
[![image](https://img.shields.io/github/contributors/xasync/damson.svg)](https://github.com/xasync/damson/graphs/contributors)

**Damson is a concise python library which aims to simplify the field validation.**

![image](https://raw.githubusercontent.com/xasync/damson/master/statics/damson-banner.jpg)

**Hold your breath! The power of Damson:**

``` {.sourceCode .python}
import damson
from damson.constraint import (Required, DataType, Between)


@damson.verify(a=[DataType(int,float)], b=[DataType(int), Between(1, 10)])
def add(a, b, ):
    return a + b


print(add(2, 3))
try:
    add(2, 3.0)
except Exception as e:
    print(e)

try:
    add(2, 10)
except Exception as e:
    print(e)


@damson.verify(**{'name': [Required(), DataType(str)], '0': [Required(), DataType(int)]})
def mix_args(name, *args):
    return '%s=%s' % (name, args)


mix_args('stone', 10, 20, 30)


@damson.verify(**{'0': [Required(), DataType(str)], '1': [Required(), DataType(int)]})
def create_kv(*args):
    return {args[0]: args[1]}


kv = create_kv('name', 10)
assert kv['name'] == 10 
```
![image](https://raw.githubusercontent.com/xasync/damson/master/statics/damson-logo.jpg)

Installation
------------

``` {.sourceCode .bash}
# Use pip
pip install damson

# Use ananconda
conda install damson
```
