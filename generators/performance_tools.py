#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
del print_function

from inspect import getsource
from timeit import default_timer as ts

from strict_functions import noglobals, strict_globals

__all__ = 'cpu_time', 'time_pipeline', 'runs_per_second'

if hasattr(iter([]), 'next'): # only python2

    from functools import partial
    from resource import getrusage, RUSAGE_SELF

    def _cpu_time(rusage):
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

    cpu_time.__doc__ = '''
    Returns the process time for profiling (sum of the kernel and user-space CPU time)
    '''

    # clean up the namespace
    del _cpu_time, partial, getrusage, RUSAGE_SELF

else: # only python3

    from time import process_time as cpu_time



@strict_globals(ts=ts, getsource=getsource)
def time_pipeline(iterable, *steps):
    '''
This times the steps in a pipeline. Give it an iterable to test against
followed by the steps of the pipeline seperated in individual functions.

Example Usage:
```
    from random import choice, randint

    l = [randint(0,50) for i in range(100)]

    step1 = lambda iterable:(i for i in iterable if i%5==0)
    step2 = lambda iterable:(i for i in iterable if i%8==3)
    step3 = lambda iterable:sorted((1.0*i)/50 for i in iterable)
    step4 = lambda iterable:(float(float(float(float(i*3)))) for i in iterable)

    print('filter first')
    time_pipeline(l, step1, step2, step3, step4)
    print('process first')
    time_pipeline(l, step3, step4, step1, step2)
    print('filter, process, filter, process')
    time_pipeline(l, step1, step3, step2, step4)
``` 

Outputs:
    filter first
    step 1 | 2.0427s | step1 = lambda iterable:(i for i in iterable if i%5==0)
    step 2 | 2.0510s | step2 = lambda iterable:(i for i in iterable if i%8==3)
    step 3 | 2.4839s | step3 = lambda iterable:sorted((1.0*i)/50 for i in iterable)
    step 4 | 2.8446s | step4 = lambda iterable:(float(float(float(float(i*3)))) for i in iterable)
    process first
    step 1 | 7.5291s | step3 = lambda iterable:sorted((1.0*i)/50 for i in iterable)
    step 2 | 20.6732s | step4 = lambda iterable:(float(float(float(float(i*3)))) for i in iterable)
    step 3 | 16.8470s | step1 = lambda iterable:(i for i in iterable if i%5==0)
    step 4 | 16.8269s | step2 = lambda iterable:(i for i in iterable if i%8==3)
    filter, process, filter, process
    step 1 | 2.0528s | step1 = lambda iterable:(i for i in iterable if i%5==0)
    step 2 | 3.3039s | step3 = lambda iterable:sorted((1.0*i)/50 for i in iterable)
    step 3 | 3.1385s | step2 = lambda iterable:(i for i in iterable if i%8==3)
    step 4 | 3.1489s | step4 = lambda iterable:(float(float(float(float(i*3)))) for i in iterable)
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


@strict_globals(ts=ts)
def runs_per_second(generator, seconds=3):
    ''' 
use this function as a profiler for both functions and generators
to see how many iterations or cycles they can run per second 

Example usage for timing simple operations/functions:

``` 
    print(runs_per_second(lambda:1+2))
    # 2074558
    print(runs_per_second(lambda:1-2))
    # 2048523
    print(runs_per_second(lambda:1/2))
    # 2075186
    print(runs_per_second(lambda:1*2))
    # 2101722
    print(runs_per_second(lambda:1**2))
    # 2104572
```

Example usage for timing iteration speed of generators:
  
``` 
    def counter():
        c = 0
        while 1:
            yield c
            c+=1

    print(runs_per_second(counter()))
    # 1697328
    print(runs_per_second((i for i in range(2000))))
    # 1591301
``` 
'''
    assert isinstance(seconds, int), 'runs_per_second needs seconds to be an int, not {}'.format(repr(seconds))
    assert seconds>0, 'runs_per_second needs seconds to be positive, not {}'.format(repr(seconds))
    # if generator is a function, turn it into a generator for testing
    if callable(generator) and not any(i in ('next', '__next__', '__iter__') for i in dir(generator)):
        try:
            # get the output of the function
            output = generator()
        except:
            # if the function crashes without any arguments
            raise Exception('runs_per_second needs a working function that accepts no arguments')
        else:
            # this usage of iter infinitely calls a function until the second argument is the output
            # so I set the second argument to something that isnt what output was.
            generator = iter(generator, (1 if output is None else None))
            del output
    c=0  # run counter, keep this one short for performance reasons
    entire_test_time_used = False
    start = ts()
    end = start+seconds
    for _ in generator:
        if ts()>end:
            entire_test_time_used = True
            break
        else:
            c += 1
    duration = (ts())-start  # the ( ) around ts ensures that it will be the first thing calculated
    return int(c/(seconds if entire_test_time_used else duration))


del getsource, noglobals, strict_globals


if __name__ == '__main__':
  
    # for timing simple operations
    print(runs_per_second(lambda:1+2))
    # 2074558
    print(runs_per_second(lambda:1-2))
    # 2048523
    print(runs_per_second(lambda:1/2))
    # 2075186
    print(runs_per_second(lambda:1*2))
    # 2101722
    print(runs_per_second(lambda:1**2))
    # 2104572
    
    # for timing iteration speed of generators
    
    def counter():
        c = 0
        while 1:
            yield c
            c+=1

    print(runs_per_second(counter()))
    # 1697328
    print(runs_per_second((i for i in range(2000))))
    # 1591301
    
    l = list(range(50))

    f1=lambda iterable:(i*2 for i in iterable if i>1)
    f2=lambda iterable:(int(str(int(str(i*3)))) for i in iterable if i<6)
    f3=lambda iterable:(i*4 for i in iterable if i%2)
    f4=lambda iterable:sorted(i*4 for i in iterable)

    def f5(iterable):
        for i in iterable:
            if i%2:
                yield i**2

    l =  (len(i) for i in open(__file__))

    from random import choice, randint

    l = [randint(0,50) for i in range(100)]

    step1 = lambda iterable:(i for i in iterable if i%5==0)
    step2 = lambda iterable:(i for i in iterable if i%8==3)
    step3 = lambda iterable:sorted((1.0*i)/50 for i in iterable)
    step4 = lambda iterable:(float(float(float(float(i*3)))) for i in iterable)

    print('filter first')
    time_pipeline(l, step1, step2, step3, step4)
    print('process first')
    time_pipeline(l, step3, step4, step1, step2)
    print('filter, process, filter, process')
    time_pipeline(l, step1, step3, step2, step4)

    
    print(runs_per_second(lambda: 1+2))

    def fn():
        return 'a' in 'hello'

    print(runs_per_second(fn))
