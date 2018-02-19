# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2018-02-19 12:01:51
# @Last Modified by:   Cody Kochmann
# @Last Modified time: 2018-02-19 12:06:31

def uniq(pipe):
    ''' this works like bash's uniq command where the generator only iterates
        if the next value is not the previous '''
    pipe = iter(pipe)
    previous = next(pipe)
    yield previous
    for i in pipe:
        if i is not previous:
            previous = i
            yield i

if __name__ == '__main__':
    l = [1,2,3,4,4,3,2,2,1,2,2]
    print(list(uniq(l)))
