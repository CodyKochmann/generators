# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2017-09-09 11:55:03
# @Last Modified 2017-10-17
# @Last Modified time: 2017-10-17 16:21:47

from functools import partial
from sys import stdin

def read(path='', mode='r', record_size=None, offset=0):
    ''' instead of writing open('file').read(), this is much more efficient '''
    if path=='': # if path is empty
        for line in stdin:
            yield line
    else:
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

if __name__ == '__main__':
    print(list(read(__file__)))
