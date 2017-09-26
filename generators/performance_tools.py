#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

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
    del _cpu_time
    del partial
    del getrusage
    del RUSAGE_SELF

else: # only python3

    from time import process_time as cpu_time


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
    from timeit import default_timer as ts
    # these store timestamps for time calculations
    durations = []
    results = []
    for i in range(len(steps)):
        i += 1
        current_tasks = steps[:i]
        #print('testing',current_tasks)
        duration = 0.0
        # run this test x number of times
        for t in range(100000):
            # build the generator
            test_generator = iter(iterable()) if callable_base else iter(iterable)
            for task in current_tasks:
                test_generator = task(test_generator)
            # time its execution
            start = ts()
            for i in test_generator:
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
    ratios = [i/sum(results) for i in results]
    #print(ratios)
    from inspect import getsource
    for i in range(len(ratios)):
        try:
            s = getsource(steps[i]).splitlines()[0].strip()
        except:
            s = repr(steps[i]).strip()
        print('step {} | {:2.4f}% | {}'.format(i+1, ratios[i]*100, s))

def runs_per_second(generator, seconds=3):
    from timeit import default_timer as ts
    c=0
    start = ts()
    end = start+seconds
    for i in generator:
        if ts()>end:
            break
        else:
            c += 1
    return int(c/seconds)


if __name__ == '__main__':
    l = list(range(50))

    f1=lambda iterable:(i*2 for i in iterable)
    f2=lambda iterable:(i*3 for i in iterable)
    f3=lambda iterable:(i*4 for i in iterable)

    def f4(iterable):
        for i in iterable:
            if i%2:
                yield i**2

    time_pipeline(l, f1, f2, f3, f3, f4)

    def counter():
        c = 0
        while 1:
            yield c
            c+=1

    print(runs_per_second(counter()))
