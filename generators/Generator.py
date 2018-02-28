# -*- coding: utf-8 -*-
# @Author: Cody Kochmann
# @Date:   2018-02-22 14:41:06
# @Last Modified 2018-02-28
# @Last Modified time: 2018-02-28 14:29:25

import sys

if sys.version_info < (3,0):
    Generator = NotImplemented
else:
    from itertools import (
        accumulate,
        combinations,
        combinations_with_replacement,
        compress,
        cycle,
        dropwhile,
        filterfalse,
        groupby,
        islice,
        permutations,
        product,
        starmap,
        takewhile,
        zip_longest
    )

    from generators import (
        all_subslices,
        all_substrings,
        alternator,
        average,
        chain,
        chunk_on,
        chunks,
        consume,
        counter,
        every_other,
        first,
        fork,
        just,
        last,
        map,
        multi_ops,
        repeater,
        side_task,
        skip,
        skip_first,
        skip_last,
        split,
        tee,
        timed_pipe,
        total,
        unfork,
        uniq,
        window
    )

    from functools import wraps

    def chainable(fn):
        @wraps(fn)
        def imma_firin(self, *mah, **lazars):
            return self.__class__(fn(self, *mah, **lazars))
        return imma_firin

    def switch_vars(fn):
        @wraps(fn)
        def imma_firin(mah, lazars):
            return fn(lazars, mah)
        return imma_firin

    class Generator(object):
        ''' generators, just more desperate to do crazy s*** '''
        def __init__(self, input_iterable):
            #print('__init__ -', locals())
            self._iterable = iter(input_iterable)

        def __iter__(self):
            return self._iterable

        def __repr__(self):
            return '< Generator - witness mah brilliance... >'

        __str__ = __repr__

        def to(self, you_want_me_to_wear_what):
            ''' use this function to convert the generator into another type '''
            assert callable(you_want_me_to_wear_what), 'Generator.to needs a callable argument'
            return you_want_me_to_wear_what(self)

        # staple madness from this library onto this class as a bunch of methods
        all_subslices  = chainable(all_subslices)
        all_substrings = chainable(all_substrings)
        alternator     = chainable(alternator)
        average        = chainable(average)
        chain          = chainable(chain)
        chunk_on       = chainable(chunk_on)
        chunks         = chainable(chunks)
        consume        = chainable(consume)
        counter        = chainable(counter)
        every_other    = chainable(every_other)
        fork           = chainable(fork)
        just           = chainable(just)
        map            = chainable(map)
        multi_ops      = chainable(multi_ops)
        repeater       = chainable(repeater)
        side_task      = chainable(side_task)
        skip           = chainable(skip)
        skip_first     = chainable(skip_first)
        skip_last      = chainable(skip_last)
        split          = chainable(split)
        tee            = chainable(tee)
        timed_pipe     = chainable(timed_pipe)
        total          = chainable(total)
        unfork         = chainable(unfork)
        uniq           = chainable(uniq)
        window         = chainable(window)

        # add the simpletons from generators that don't return iterables
        first = lambda self, i=1:first(self, i) if i==1 else Generator(first(self, i))
        last = lambda self, i=1:last(self, i) if i==1 else Generator(last(self, i))

        # F*** it lets add stuff from itertools!!!
        accumulate                    = chainable(accumulate)
        combinations                  = chainable(combinations)
        combinations_with_replacement = chainable(combinations_with_replacement)
        compress                      = chainable(compress)
        cycle                         = chainable(cycle)
        groupby                       = chainable(groupby)
        islice                        = chainable(islice)
        permutations                  = chainable(permutations)
        product                       = chainable(product)

        # functions that need a little arg resorting
        filterfalse = lambda self, fn:Generator(filterfalse(fn, self))
        dropwhile = lambda self, fn:Generator(dropwhile(fn, self))
        starmap = lambda self, fn:Generator(starmap(fn, self))
        takewhile = lambda self, fn:Generator(takewhile(fn, self))

        # add keywords from python's builtins
        filter = lambda self, fn:Generator(filter(fn, self))
        sort = lambda self:Generator(sorted(self))
        max = lambda self:max(self)
        sum = lambda self:sum(self)

    if __name__ == '__main__':
        true_og = (i for i in range(10))

        print(
            #Generator(i for i in range(10)).window(3).chunks(2) #.first()
            Generator(i for i in range(10)).window(3).skip().skip().islice(4,8).to(list)
        )

        # pe 1 - sum of multiples of 3 and 5 up to 1000
        print(
            'pe-1',
            sum(Generator(range(1000)).filterfalse(lambda i:i%3 and i%5))
        )
        print(
            'pe-1',
            #sum(Generator(range(0, 1000, 3)).chain(range(0, 1000, 5)).to(set))
            Generator(range(0, 1000, 3)).chain(range(0, 1000, 5)).sum()
        )
        exit()

        # pe 3 - largest prime factor for 600851475143
        print(
            'pe-3',
            Generator(
                count(1)
            ).map(
                lambda i:int(600851475143/i)
            ).uniq().filter(
                isPrime
            ).first()
        )



