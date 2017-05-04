
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

### timer.py
```python
from started import started

@started
def timer():
    """ generator that tracks time """
    start_time = time()
    previous = start_time
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

