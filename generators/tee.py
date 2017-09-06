# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2017-05-05 16:25:49
# @Last Modified by:   Cody Kochmann
# @Last Modified time: 2017-05-05 16:33:53

from __future__ import print_function

def tee(pipeline, name, output_function=print):
    for i in pipeline:
        output_function('{} - {}'.format(name,i))
        yield i

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
