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
    del _cpu_time, partial, getrusage, RUSAGE_SELF

else: # only python3

    from time import process_time as cpu_time


@strict_globals(ts=ts, getsource=getsource)
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
    ''' use this function as a profiler for both functions and generators
    to see how many iterations or cycles they can run per second '''
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
    print(runs_per_second(lambda:1+2))
    print(runs_per_second(lambda:1-2))
    print(runs_per_second(lambda:1/2))
    print(runs_per_second(lambda:1*2))
    print(runs_per_second(lambda:1**2))

    print(runs_per_second((i for i in range(2000))))

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

    #time_pipeline(l, f1, f2, f3, f3, f4, f5)
    #time_pipeline(l, *(choice([f1,f2,f3]) for i in range(10)))
    """time_pipeline(
                    l,
                    f2,
                    f3,
                    f1,
                    f3,
                    f2,
                    f3,
                    f3,
                    f3,
                    f3,
                    f3,
                )"""





    def counter():
        c = 0
        while 1:
            yield c
            c+=1

    print(runs_per_second(counter()))

    print(runs_per_second(lambda: 1+2))

    def fn():
        return 'a' in 'hello'

    print(runs_per_second(fn))
