# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2017-05-05 16:25:49
# @Last Modified 2017-10-05e>
# @Last Modified time: 2017-12-09 13:24:12

from __future__ import print_function
del print_function
from strict_functions import noglobals

@noglobals
def tee(pipeline, name, output_function=print):
    for i in pipeline:
        output_function('{} - {}'.format(name,i))
        yield i

del noglobals

if __name__ == '__main__':
    gen = (i for i in range(100))
    gen = tee(gen,'step1')

    gen = (i*2 for i in gen)
    gen = tee(gen,'step2')

    gen = (i**2 for i in gen)
    gen = tee(gen,'step3')

    gen = (i/2 for i in gen)
    gen = tee(gen,'step4')

    # run the generator
    print(list(i for i in gen))
