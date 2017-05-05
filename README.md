
# generators
Where all of my generator tricks are collected!

### average.py
```python
from started import started

@started
def average():
    """ generator that holds a rolling average """
    count = 0.0
    total = generators.sum()
    i=0
    while 1:
        i = yield (total.send(i)*1.0/count if count else 0)
        count += 1
```

### counter.py
```python
from started import started

@started
def counter():
    "generator that holds a sum"
    c = 0
    while 1:
        yield c
        c += 1
```

### fork.py
```python
def fork(g,c=2):
    """ fork a generator in python """
    return ((i,)*c for i in g)
```

### multi_ops.py
```python
def multi_ops(data_stream, *funcs):
    """ fork a generator with multiple operations/functions

        data_stream  -  an iterable data structure (ie: list/generator/tuple)
        funcs        -  every function that will be applied to the data_stream """

    assert all(callable(func) for func in funcs), 'multi_ops can only apply functions to the first argument'
    assert len(funcs), 'multi_ops needs at least one function to apply to data_stream'

    for i in data_stream:
        if len(funcs) > 1:
            yield tuple(func(i) for func in funcs)
        elif len(funcs) == 1:
            yield funcs[0](i)

```

### read_file.py
```python
def read_file(path):
    ''' reads a file into a line generator '''
    with open(path) as f:
        for line in f:
            yield line
```

### started.py
```python

def started(generator_function):
    """ starts a generator when created """
    def wrapper(*args, **kwargs):
        g = generator_function(*args, **kwargs)
        next(g)
        return g
    return wrapper
```

### tee.py
```python
from __future__ import print_function

def tee(pipeline, name, output_function=print):
    for i in pipeline:
        output_function('{} - {}'.format(name,i))
        yield i

```

### timer.py
```python
from started import started
from time import time

@started
def timer():
    """ generator that tracks time """
    start_time = time()
    while 1:
        yield time()-start_time

```

### total.py
```python
from started import started

@started
def total():
    "generator that holds a total"
    total = 0
    while 1:
        total += yield total
```

### unfork.py
```python
def unfork(g):
    """ returns a generator with one output at a time if
        multiple outputs are coming out of the given """
    for i in g:
        for x in i:
            yield x
```

