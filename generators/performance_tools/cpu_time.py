#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This is a universal python2 and python3 version of time.process_time.
'''

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
