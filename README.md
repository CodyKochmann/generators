
# Generators
Where all of my generator tricks are collected!

## How to install it?

```
pip install generators
```

### generators.all_substrings
```python
def all_substrings(s):
    ''' yields all substrings of a string '''
    join = partial(''.join)
    for i in range(1, len(s) + 1):
        for sub in window(s, i):
            yield join(sub)
```

### generators.average
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

### generators.chain
```python
def chain(*a):
    """itertools.chain, just better"""
    for g in a:
        if hasattr(g, '__iter__'):
            # iterate through if its iterable
            for i in g:
                yield i
        else:
            # just yield the whole thing if its not
            yield g
```

### generators.chunks
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

### generators.counter
```python
@started
def counter():
    "generator that holds a sum"
    c = 0
    while 1:
        yield c
        c += 1
```

### generators.fork
```python
def fork(g,c=2):
    """ fork a generator in python """
    return ((i,)*c for i in g)
```

### generators.itemgetter
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

### generators.iter_kv
```python
def iter_kv(d):
    ''' does what dict.items() does, without wasting memory '''
    for k in d:
        yield k, d[k]
```

### generators.multi_ops
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

### generators.read
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

### generators.read_file
```python
def read_file(path):
    ''' reads a file into a line generator '''
    with open(path) as f:
        for line in f:
            yield line
```

### generators.started
```python
def started(generator_function):
    """ starts a generator when created """
    def wrapper(*args, **kwargs):
        g = generator_function(*args, **kwargs)
        next(g)
        return g
    return wrapper
```

### generators.tee
```python
def tee(pipeline, name, output_function=print):
    for i in pipeline:
        output_function('{} - {}'.format(name,i))
        yield i
```

### generators.timer
```python
@started
def timer():
    """ generator that tracks time """
    start_time = time()
    while 1:
        yield time()-start_time
```

### generators.total
```python
@started
def total():
    "generator that holds a total"
    total = 0
    while 1:
        total += yield total
```

### generators.unfork
```python
def unfork(g):
    """ returns a generator with one output at a time if
        multiple outputs are coming out of the given """
    for i in g:
        for x in i:
            yield x
```

### generators.window
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
    if len(d) == d.maxlen:
        # yield the windows
        for i in iterable:
            yield tuple(d)
            d.append(i)
        yield tuple(d)
```

