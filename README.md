
# Generators
Where all of my generator tricks are collected!

## How to install it?

```
pip install generators
```

### generators.all_subslices
```python
sys.path.append(os.path.dirname(__file__))
del sys
del os
def all_subslices(itr):
    """ generates every possible slice that can be generated from an iterable """
    assert iterable(itr), 'generators.all_subslices only accepts iterable arguments, not {}'.format(itr)
    if not hasattr(itr, '__len__'): # if this isnt materialized, make it a list
        itr = list(itr)
    len_itr = len(itr)
    for start,_ in enumerate(itr):
        d = deque()
        for i in islice(itr, start, len_itr): # how many slices for this round
            d.append(i)
            yield tuple(d)
```

### generators.all_substrings
```python
def all_substrings(s):
    ''' yields all substrings of a string '''
    join = ''.join
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
def chain(*args):
    """itertools.chain, just better"""
    has_iter = partial(hasattr, name='__iter__')
    # check if a single iterable is being passed for
    # the case that it's a generator of generators
    if len(args) == 1 and hasattr(args[0], '__iter__'):
        args = args[0]
    for arg in args:
        # if the arg is iterable
        if hasattr(arg, '__iter__'):
            # iterate through it
            for i in arg:
                yield i
        # otherwise
        else:
            # yield the whole argument
            yield arg
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

### generators.early_warning
```python
def early_warning(iterable):
    nxt = None
    prev = next(iterable)
    while 1:
        try:
            nxt = next(iterable)
        except:
            warning('this generator is now empty')
            yield prev
            break
        else:
            yield prev
            prev = nxt
```

### generators.fork
```python
def fork(g,c=2):
    """ fork a generator in python """
    return ((i,)*c for i in g)
```

### generators.inline_tools
```python
del print_function
__all__ = 'asserts', 'print'
_print = print
def asserts(input_args, rule, message=''):
    """ this function allows you to write asserts in generators since there are
        moments where you actually want the program to halt when certain values
        are seen.
    """
    assert callable(rule), 'asserts needs rule to be a callable function'
    assert type(message).__name__ in ('str', 'unicode'), 'asserts needs message to be a string'
    if message == '':
        try:
            s = getsource(rule).splitlines()[0].strip()
        except:
            s = repr(rule).strip()
        message = 'illegal input of {} breaks - {}'.format(input_args, s)
    assert rule(input_args), message
    return input_args
def print(*a):
    """ print just one that returns what you give it instead of None """
    try:
        _print(*a)
        return a[0] if len(a) == 1 else a
    except:
        _print(*a)
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
    ''' iterate through massive dictionaries without the slowdown and memory usage of dict.items '''
    for k in d:
        yield k, d[k]
```

### generators.iterable
```python
def iterable(target):
    ''' returns true if the given argument is iterable '''
    if any(i in ('next', '__next__', '__iter__') for i in dir(target)):
        return True
    else:
        try:
            iter(target)
            return True
        except:
            return False
```

### generators.just
```python
def just(*args):
    ''' this works as an infinite loop that yields
        the given argument(s) over and over
    '''
    assert len(args) >= 1, 'generators.just needs at least one arg'
    if len(args) == 1: # if only one arg is given
        try:
            # try to cycle in a set for iteration speedup
            return cycle(set(args))
        except:
            # revert to cycling args as a tuple
            return cycle(args)
    else:
        return cycle({args})
```

### generators.loop
```python
def loop():
    '''
    use this for infinite iterations with
        for _ in loop():
    instead of:
        while True:
    to get a free speedup in loops.
    '''
    return cycle({0})
```

### generators.map
```python
"""
what does map do
- run first argument (the function) against the input iterables
- if multiple iterables are defined, multiple inputs are required for the function
what does our map do
- run multi-ops if multiple functions are given
- run window or chunks if multiple args in function
"""
def function_arg_count(fn):
    """ generates a list of the given function's arguments """
    assert callable(fn), 'function_arg_count needed a callable function, not {0}'.format(repr(fn))
    if hasattr(fn, '__code__') and hasattr(fn.__code__, 'co_argcount'):
        return fn.__code__.co_argcount
    else:
        return 1 # not universal, but for now, enough... :/
def map(*args):
    """ this map works just like the builtin.map, except, this one you can also:
        - give it multiple functions to map over an iterable
        - give it a single function with multiple arguments to run a window
          based map operation over an iterable
    """
    #print(args)
    functions_to_apply = [i for i in args if callable(i)]
    iterables_to_run = [i for i in args if not callable(i)]
    #print('functions_to_apply:',functions_to_apply)
    #print('iterables_to_run:',iterables_to_run)
    assert len(functions_to_apply)>0, 'at least one function needs to be given to map'
    assert len(iterables_to_run)>0, 'no iterables were given to map'
    # check for native map usage
    if len(functions_to_apply) == 1 and len(iterables_to_run) >= 1 and map.function_arg_count(*functions_to_apply)==1:
        if hasattr(iter([]), '__next__'): # if python 3
            return __builtins__.map(functions_to_apply[0], *iterables_to_run)
        else:
            return iter(__builtins__.map(functions_to_apply[0], *iterables_to_run))
    # ---------------------------- new logic below ----------------------------
    # logic for a single function
    elif len(functions_to_apply) == 1:
        fn = functions_to_apply[0]
        # if there is a single iterable, chop it up
        if len(iterables_to_run) == 1:
            return (fn(*i) for i in window(iterables_to_run[0], map.function_arg_count(functions_to_apply[0])))
    # logic for more than 1 function
    elif len(functions_to_apply) > 1 and len(iterables_to_run) == 1:
        return multi_ops(*(iterables_to_run + functions_to_apply))
    else:
        raise ValueError('invalid usage of map()')
map.function_arg_count = function_arg_count
del function_arg_count
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

### generators.performance_tools
```python
del print_function
__all__ = 'cpu_time', 'time_pipeline', 'runs_per_second'
if hasattr(iter([]), 'next'): # only python2
    def _cpu_time(rusage):
        ''' just like python3's time.process_time :
            Process time for profiling: sum of the kernel and user-space CPU time.
        '''
        usage = rusage()
        return usage.ru_utime + usage.ru_stime
    # i used a nested partial because access to the arguments is
    # faster than doing global lookups and I didn't want to allow
    # access to manipulate that variable so a partial hid it.
    #
    # for those who agree that the code below is ugly, this is
    # pretty much optimizing this call into cpu_time:
    #
    #   _cpu_time(getrusage(RUSAGE_SELF))
    #
    cpu_time = partial(_cpu_time, partial(getrusage, RUSAGE_SELF))
    # clean up the namespace
    del _cpu_time
    del partial
    del getrusage
    del RUSAGE_SELF
else: # only python3
def time_pipeline(iterable, *steps):
    ''' this times the steps in a pipeline.
        give it an iterable to test against
        followed by the steps of the pipeline
        seperated in individual functions.
    '''
    if callable(iterable):
        try:
            iter(iterable())
            callable_base = True
        except:
            raise TypeError('time_pipeline needs the first argument to be an iterable or a function that produces an iterable.')
    else:
        try:
            iter(iterable)
            callable_base = False
        except:
            raise TypeError('time_pipeline needs the first argument to be an iterable or a function that produces an iterable.')
    # if iterable is not a function, load the whole thing
    # into a list so it can be ran over multiple times
    if not callable_base:
        iterable = tuple(iterable)
    # this is used for timestamps
    # these store timestamps for time calculations
    durations = []
    results = []
    for i,_ in enumerate(steps):
        current_tasks = steps[:i+1]
        #print('testing',current_tasks)
        duration = 0.0
        # run this test x number of times
        for t in range(100000):
            # build the generator
            test_generator = iter(iterable()) if callable_base else iter(iterable)
            # time its execution
            start = ts()
            for task in current_tasks:
                test_generator = task(test_generator)
            for i in current_tasks[-1](test_generator):
                pass
            duration += ts() - start
        durations.append(duration)
        if len(durations) == 1:
            results.append(durations[0])
            #print(durations[0],durations[0])
        else:
            results.append(durations[-1]-durations[-2])
            #print(durations[-1]-durations[-2],durations[-1])
    #print(results)
    #print(durations)
    assert sum(results) > 0
    resultsum = sum(results)
    ratios = [i/resultsum for i in results]
    #print(ratios)
    for i in range(len(ratios)):
        try:
            s = getsource(steps[i]).splitlines()[0].strip()
        except:
            s = repr(steps[i]).strip()
        print('step {} | {:2.4f}s | {}'.format(i+1, durations[i], s))
def runs_per_second(generator, seconds=3):
    # if generator is a function, turn it into a generator for testing
    if callable(generator) and not any(i in ('next', '__next__', '__iter__') for i in dir(generator)):
        try:
            output = generator()
        except:
            raise Exception('runs_per_second needs a working function that accepts no arguments')
        else:
            if output is None:
                breakpoint = ''
            else:
                breakpoint = None
            del output
            generator = iter(generator, breakpoint)
    c=0
    start = ts()
    end = start+seconds
    for i in generator:
        if ts()>end:
            break
        else:
            c += 1
    return int(c/seconds)
```

### generators.read
```python
def read(path, mode='r', record_size=None, offset=0):
    ''' instead of writing open('file').read(), this is much more efficient '''
    with open(path, mode) as f:
        if record_size is None:  # no record_size? iterate over lines
            for line in f:
                if offset > 0:
                    offset -= 1
                else:
                    yield line
        else:  # if record_size is specified, iterate over records at that size
            stop_value = b'' if mode == 'rb' else ''
            f.seek(offset)
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

### generators.rps
```python
""" this behaves as a shortcut for the rps function in performance_tools """
sys.path.append(os.path.dirname(__file__))
del sys
del os
```

### generators.side_task
```python
del print_function
sys.path.append(os.path.dirname(__file__))
del sys
del os
def side_task(pipe, *side_jobs):
    ''' allows you to run a function in a pipeline without affecting the data '''
    # validate the input
    assert iterable(pipe), 'side_task needs the first argument to be iterable'
    for sj in side_jobs:
        assert callable(sj), 'all side_jobs need to be functions, not {}'.format(sj)
    # add a pass through function to side_jobs
    side_jobs = (lambda i:i ,) + side_jobs
    # run the pipeline
    for i in map(pipe, *side_jobs):
        yield i[0]
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
del print_function
def tee(pipeline, name, output_function=print):
    for i in pipeline:
        output_function('{} - {}'.format(name,i))
        yield i
```

### generators.timed_pipe
```python
def timed_pipe(generator, seconds=3):
    ''' This is a time limited pipeline. If you have a infinite pipeline and
        want it to stop yielding after a certain amount of time, use this! '''
    # grab the highest precision timer
    # when it started
    start = ts()
    # when it will stop
    end = start + seconds
    # iterate over the pipeline
    for i in generator:
        # if there is still time
        if ts() < end:
            # yield the next item
            yield i
        # otherwise
        else:
            # stop
            break
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

