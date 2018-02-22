# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2018-02-17 10:41:19
# @Last Modified 2018-02-22e>
# @Last Modified time: 2018-02-22 15:58:25

from collections import deque
from skip import skip
from window import window
from chain import chain

def split(pipe, splitter, skip_empty=False):
    ''' this function works a lot like groupby but splits on given patterns,
        the same behavior as str.split provides. if skip_empty is True,
        split only yields pieces that have contents

        Example:

            splitting 1011101010101
            by        10
            returns   ,11,,,,1

        Or if skip_empty is True

            splitting 1011101010101
            by        10
            returns   11,1
    '''

    splitter = tuple(splitter)
    len_splitter = len(splitter)
    pipe=iter(pipe)
    current = deque()
    tmp = []
    windowed = window(pipe, len(splitter))
    for i in windowed:
        if i == splitter:
            skip(windowed, len(splitter)-1)
            yield list(current)
            current.clear()
            tmp = []
        else:
            current.append(i[0])
            tmp = i
    if len(current) or len(tmp):
        yield list(chain(current,tmp))

if __name__ == '__main__':
    print(list(split(''.join(map(str,range(10))),'345')))
