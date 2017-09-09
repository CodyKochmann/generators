
# Generators
Where all of my generator tricks are collected!

## How to install it?

```
pip install generators
```

### all_substrings.py
```python
def all_substrings(s):
    ''' yields all substrings of a string '''
    join = partial(''.join)
    for i in range(1, len(s) + 1):
        for sub in window(s, i):
            yield join(sub)
```

### average.py
```python
@started
def average():
    """ generator that holds a rolling average """
    count = 0
    total = total()
    i=0
    while 1:
        i = yield ((total.send(i)*1.0)/count if count else 0)
        count += 1
```

### chunks.py
```python
def chunks(iterable, chunk_size, output_type=tuple):
    ''' returns chunks of an iterable '''
    chunk = deque(maxlen=chunk_size)
    for i in iterable:
        chunk.append(i)
        if len(chunk) == chunk_size:
            yield output_type(chunk)
            chunk.clear()
    if len(chunk):
        yield output_type(chunk)
```

### counter.py
```python
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

### itemgetter.py
```python
def itemgetter(iterable, indexes):
    ''' same functionality as operator.itemgetter except, this one supports
        both positive and negative indexing of generators as well '''
    assert type(indexes)==tuple, 'indexes needs to be a tuple of ints'
    assert all(type(i)==int for i in indexes), 'indexes needs to be a tuple of ints'
    positive_indexes=[i for i in indexes if i>=0]
    negative_indexes=[i for i in indexes if i<0]
    out = {}
    if len(negative_indexes):
        # if there are any negative indexes
        negative_index_buffer = deque(maxlen=min(indexes)*-1)
        for i,x in enumerate(iterable):
            if i in positive_indexes:
                out[i]=x
            negative_index_buffer.append(i)
        out.update({ni:negative_index_buffer[ni] for ni in negative_indexes})
    else:
        # if just positive results
        out.update({i:x for i,x in enumerate(iterable) if i in positive_indexes})
    return itemgetter(*indexes)(out)
```

### iter_kv.py
```python
def iter_kv(d):
    ''' does what dict.items() does, without wasting memory '''
    for k in d:
        yield k, d[k]
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

### read.py
```python
def read(path, mode='r', record_size=None):
    ''' instead of writing open('file').read(), this is much more efficient '''
    with open(path, mode) as f:
        if record_size is None:  # no record_size? iterate over lines
            for line in f:
                yield line
        else:  # if record_size is specified, iterate over records at that size
            stop_value = b'' if mode == 'rb' else ''
            for record in iter(partial(f.read, record_size), stop_value):
                yield record
    # before this generator raises StopIteration, it will
    # close the file since we are using a context manager.
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
def tee(pipeline, name, output_function=print):
    for i in pipeline:
        output_function('{} - {}'.format(name,i))
        yield i
```

### timer.py
```python
@started
def timer():
    """ generator that tracks time """
    start_time = time()
    while 1:
        yield time()-start_time
```

### total.py
```python
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

### window.py
```python
def window(iterable, size):
    ''' yields wondows of a given size '''
    d = deque(maxlen=size)
    # normalize iterable into a generator
    iterable = (i for i in iterable)
    # fill d until full
    for i in iterable:
        d.append(i)
        if len(d) == size:
            break
    # yield the windows
    for i in iterable:
        yield tuple(d)
        d.append(i)
    yield tuple(d)
```

