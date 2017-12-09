# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2017-09-09 11:55:03
# @Last Modified 2017-10-17
# @Last Modified time: 2017-12-09 13:18:02

from functools import partial
from sys import stdin

from strict_functions import strict_globals

@strict_globals(partial=partial)
def read_with_seperator(f, seperator, stop_value):
    assert hasattr(f, 'read')
    assert isinstance(stop_value, str)
    assert isinstance(seperator, str)
    assert len(seperator)

    out = stop_value

    for i in iter(partial(f.read, 1), stop_value):
        out += i
        if seperator in out:
            yield out
            out = stop_value

@strict_globals(partial=partial, stdin=stdin, read_with_seperator=read_with_seperator)
def read(path='', mode='r', record_size=None, record_seperator=None, offset=0, autostrip=False):
    ''' instead of writing open('file').read(), this is much more efficient and has some extra goodies '''
    assert isinstance(path, str), 'path needs to be a string, not: {}'.format(repr(path))
    assert isinstance(mode, str), 'mode needs to be a string, not: {}'.format(repr(mode))
    assert ((record_size is None)+(record_seperator is None))>0 , 'generators.read does not support both record_seperator and record_size options being used at the same time: {} {}'.format(record_size, record_seperator)
    assert record_size is None or type(record_size) is int, 'record_size can only be defined as an int, not: {}'.format(repr(record_size))
    assert record_seperator is None or isinstance(record_seperator, str) and len(record_seperator), 'record_seperator can only be defined as a non-empty string, not: {}'.format(repr(record_seperator))
    assert type(offset) == int and offset>=0, 'offset needs to be a positive int, not: {}'.format(repr(offset))
    assert type(autostrip) == bool, 'autostrip needs to be a boolean, not: {}'.format(repr(autostrip))

    stop_value = b'' if mode == 'rb' else ''
    if autostrip:
        autostrip = lambda i:i.strip()
    else:
        autostrip = lambda i:i

    if path=='': # if path is empty, use stdin
        if record_seperator is None:
            for line in stdin:
                yield autostrip(line)
        else:
            for entry in read_with_seperator(stdin, record_seperator, stop_value):
                yield autostrip(entry)
    else: # otherwise, open path
        with open(path, mode) as f:
            if record_size is None and record_seperator is None:  # no record_size or record_seperator? iterate over lines
                for line in f:
                    if offset > 0: # offset in line reading mode offsets per each line
                        offset -= 1
                    else:
                        yield autostrip(line)
            elif record_seperator is not None:
                f.seek(offset)
                for record in read_with_seperator(f, record_seperator, stop_value):
                    yield autostrip(record)
            else:  # if record_size is specified, iterate over records at that size
                f.seek(offset)
                for record in iter(partial(f.read, record_size), stop_value):
                    yield autostrip(record)
        # before this generator raises StopIteration, it will
        # close the file since we are using a context manager.

del partial, stdin, strict_globals, read_with_seperator

if __name__ == '__main__':
    def bar():
        print('-'*40)
    if 1: # standard read
        for i in read(__file__):
            bar()
            print(i)
    if 1: # custom record seperator
        for i in read(__file__, record_seperator='a'):
            bar()
            print(i)
    if 1: # custom record size
        for i in read(__file__, record_size=2):
            bar()
            print(i)
    if 1: # custom offset
        for i in read(__file__, offset=50):
            bar()
            print(i)
    if 1: # custom offset with autostrip
        for i in read(__file__, offset=50, autostrip=True):
            bar()
            print(i)

