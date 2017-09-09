# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2017-09-09 11:55:03
# @Last Modified by:   Cody Kochmann
# @Last Modified time: 2017-09-09 12:37:35

from functools import partial


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
