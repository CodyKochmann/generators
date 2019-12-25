from __future__ import print_function
from functools import wraps, partial
from strict_functions import overload, attempt
from inspect import getsource
import itertools
from itertools import permutations, islice
import sys
import os
import operator

import generators
from generators import iterable, consume, itemgetter, rps

class OrderError(Exception):
    pass

class Generator:
    def __init__(self, input_iterable):
        #print('__init__ -', locals())
        self._iterable = iter(input_iterable)

    def __iter__(self):
        return self._iterable

    def __repr__(self):
        return '<Generator with frickin laser beams at {}>'.format(hex(id(self)))

    __str__ = __repr__

    def to(self, you_want_me_to_wear_what):
        ''' use this function to convert the generator into another type '''
        assert callable(you_want_me_to_wear_what), 'Generator.to needs a callable argument'
        return you_want_me_to_wear_what(self)

    @staticmethod
    def __chainable_method__(fn):
        @wraps(fn)
        def wrapper(*a, **k):
            out = fn(*a, **k)
            if iterable(out):
                return Generator(out)
            else:
                return out
        return wrapper

    @staticmethod
    def __grab_first__(t, l):
        if type(t)==type:
            check = lambda i, t=t:isinstance(i, t)
        elif callable(t):
            check = t
        else:
            raise ValueError('t({}) is not a function or type'.format(t))
        for i,v in enumerate(list(l)):
            if check(v):
                return l.pop(i)
        raise OrderError()

    @staticmethod
    def __require_args__(count, args):
        if count!=len(args):
            raise ValueError(
                'wrong arg count\nneeded\n    {} args\nreceived\n    {} args\nraw\n    {}'.format(
                    count,
                    len(args),
                    repr(tuple(args))
                )
            )

    @staticmethod
    def __printable_fn__(fn):
        fn_repr = repr(fn)
        return attempt(
                partial(getsource, fn),
                fn_repr
            ) if '<lambda' in fn_repr else (
                getattr(fn, '__name__', fn_repr)
            )

    @staticmethod
    def __organize_args__(arg_pattern, args, fn=None, name=None):
        _args = args[:]
        Generator.__require_args__(len(arg_pattern), args)
        try:
            return list(map(
                partial(
                    Generator.__grab_first__,
                    l=args[:]
                ),
                arg_pattern
            ))
        except OrderError:
            if fn is not None:
                # this is for clean debugging
                _og_args = repr(tuple(args[:]))
                # try other combinations
                for i in permutations(args):
                    try:
                        return Generator.__organize_args__(
                            arg_pattern,
                            list(i),
                        )
                    except OrderError:
                        pass
                raise ValueError(
                    '-\ncouldnt find a valid ordering for:\n    Generator.{}\nrequired:\n    {}\nrecieved:\n    {}'.format(
                        name,
                        '\n    '.join(
                            map(
                                Generator.__printable_fn__, arg_pattern
                            )
                        ),
                        _og_args
                    )
                )
            else:
                raise OrderError()

    @staticmethod
    def add_method(fn, arg_pattern, name=None, chainable=True):
        if name is None:
            name = fn.__name__
        @wraps(fn)
        def method(*args):
            return fn(*Generator.__organize_args__(
                arg_pattern,
                list(args),
                fn,
                name=name
            ))
        if chainable:
            method = wraps(fn)(Generator.__chainable_method__(method))
        if hasattr(Generator, name):
            method = overload(
                method,
                getattr(Generator, name)
            )
        setattr(
            Generator,
            name,
            method
        )

    @staticmethod
    def add_methods(methods_to_add):
        ''' use this to bulk add new methods to Generator '''
        for i in methods_to_add:
            try:
                Generator.add_method(*i)
            except Exception as ex:
                raise Exception('issue adding {} - {}'.format(repr(i), ex))

    def __next__(self):
        return next(self._iterable)

    def next(self):
        return next(self._iterable)

    def print(self, before='', use_repr=False, **print_options):
        return Generator(self.side_task((
            lambda i:print('{}{}'.format(before, repr(i)), **print_options)
        ) if use_repr else (
            lambda i:print('{}{}'.format(before, i), **print_options)
        )))

    benchmark = rps

    #def __slice__(self, s):
    #    raise NotImplementedError()
    def __negative_slice__(self, s):
        if s.step is None:
            return {#start,stop
                    (None, False):lambda:(self.last(abs(s.stop))), # [:-1]
                    (False, None):lambda:(self.skip_last(abs(s.start))), # [-1:]
                    (True, False):lambda:(self.skip(s.start).skip_last(abs(s.stop))), # [5:-1]
                    (False, True):lambda:(self.last(abs(s.start)).first(s.stop)),  # [-10:6]
                    (False,False):lambda:(self.last(abs(s.start)).skip_last(abs(s.stop)))  # [-5:-1]
            }[tuple(map((lambda i:None if i is None else i>0), [s.start, s.stop]))]()
        else:
            raise NotImplemented("This will be possible once I can map out all the possibilities")

    def __getitem__(self, a):
        if isinstance(a, slice):
            return Generator((
                islice(self, a.start, a.stop, a.step)
            ) if all(i is None or 0<i for i in (a.start, a.stop, a.step)) else (
                self.__negative_slice__(a)
            ))
        elif isinstance(a, int):
            # get single item
            if a == 0:
                return next(self)
            elif a > 0:
                return next(self.skip(a-1))
            elif a < 0:
                return next(self.last(abs(a)))
        elif isinstance(a, tuple): # multi-item slice
            return Generator(generators.itemgetter(self, a))
        else:
            raise ValueError('invalid slice argument - {}'.format(repr(a)))

# add the stuff from generators
Generator.add_methods([
    [generators.map, [Generator, callable]],
    [generators.map, [Generator, callable, callable]],
    [generators.map, [Generator, callable, callable, callable]],
    [generators.map, [Generator, callable, callable, callable, callable]],
    [generators.map_parallel, [Generator, callable, int]],
    [generators.map_multithread, [Generator, callable, int]],
    [generators.map_multicore, [Generator, callable, int]],

    [generators.all_subslices, [Generator]],
    [generators.all_substrings, [Generator]],
    [generators.alternator, [Generator, iterable], 'alternate'],
    [generators.alternator, [Generator, iterable, iterable], 'alternate'],
    [generators.alternator, [Generator, iterable, iterable, iterable], 'alternate'],
    [generators.apply_to_last, [Generator, callable]],
    [generators.chain, [Generator]],
    [generators.chain, [Generator, iterable]],
    [generators.chain, [Generator, iterable, iterable]],
    [generators.chain, [Generator, iterable, iterable, iterable]],
    [generators.chunks, [Generator, int], 'chunk'],
    [generators.chunk_on, [Generator, callable]],
    [generators.consume, [Generator]],  # leave this one here for backwards compatability
    [generators.consume, [Generator], 'run'],
    [generators.every_other, [Generator, int]],
    [generators.first, [Generator]],
    [generators.first, [Generator, int]],
    [generators.fork, [Generator, int]],
    [generators.iterable, [object]],
    [generators.last, [Generator]],
    [generators.last, [Generator, int]],
    [generators.multi_ops, [Generator, callable]],
    [generators.multi_ops, [Generator, callable, callable]],
    [generators.multi_ops, [Generator, callable, callable, callable]],
    [generators.multi_ops, [Generator, callable, callable, callable, callable]],
    [generators.repeater, [Generator], 'repeat'],
    [generators.repeater, [Generator, int], 'repeat'],
    [generators.reverse, [Generator]],
    [generators.side_task, [Generator, callable]],
    [generators.side_task, [Generator, callable, callable]],
    [generators.side_task, [Generator, callable, callable, callable]],
    [generators.side_task, [Generator, callable, callable, callable, callable]],
    [generators.skip, [Generator]],
    [generators.skip, [Generator, int]],
    [generators.skip_first, [Generator]],
    [generators.skip_first, [Generator, int]],
    [generators.skip_last, [Generator]],
    [generators.skip_last, [Generator, int]],
    [generators.split, [Generator, iterable]],
    [generators.split, [Generator, iterable, bool]],
    [generators.switch, [Generator, callable, dict]],
    [generators.switch, [Generator, callable, dict, callable]],
    [generators.tee, [Generator, str]],
    [generators.tee, [Generator, str, callable]],
    [generators.timed_pipe, [Generator], 'timed'],
    [generators.timed_pipe, [Generator, int], 'timed'],
    [generators.timed_pipe, [Generator], 'time_limit'],
    [generators.timed_pipe, [Generator, int], 'time_limit'],
    [generators.unfork, [Generator]],
    [generators.uniq, [Generator]],
    [generators.window, [Generator]],
    [generators.window, [Generator, int]]
])
# add the stuff from builtins
Generator.add_methods([
    [lambda g,k=None:(i for i in sorted(g, key=k)), [Generator], 'sort'],
    [lambda g,k=None:(i for i in sorted(g, key=k)), [Generator, callable], 'sort'],
    [max, [Generator], None, False],
    [min, [Generator], None, False],
    [sum, [Generator], None, False],
    [enumerate, [Generator]]
])

def _accumulate(iterable, func=(lambda a,b:a+b)): # this was from the itertools documentation
    'Return running totals'
    # accumulate([1,2,3,4,5]) --> 1 3 6 10 15
    # accumulate([1,2,3,4,5], operator.mul) --> 1 2 6 24 120
    it = iter(iterable)
    try:
        total = next(it)
    except StopIteration:
        return
    yield total
    for element in it:
        total = func(total, element)
        yield total

# add stuff from itertools
Generator.add_methods([
    [itertools.compress, [Generator, iterable]],
    [itertools.dropwhile, [callable, Generator]],
    [itertools.groupby, [Generator, callable]],
    [itertools.takewhile, [callable, Generator]],
    [itertools.permutations, [Generator]],
    [itertools.combinations, [Generator]],
    [itertools.permutations, [Generator, int]],
    [itertools.combinations, [Generator, int]],
    [itertools.combinations_with_replacement, [Generator, int]],
    [(lambda g,r:itertools.product(g, repeat=r)), [Generator, int], 'product'],
    [(lambda g,r:itertools.product(g, repeat=r)), [Generator], 'product'],
    [filter, [callable, Generator]],
    [getattr(itertools, 'accumulate', _accumulate), [Generator, callable], 'accumulate'],
    [getattr(itertools, 'accumulate', _accumulate), [Generator], 'accumulate'],
    [getattr(itertools, 'ifilter', filter), [callable, Generator], 'filter'],
    [getattr(itertools, 'filterfalse', getattr(itertools, 'ifilterfalse', (lambda f,g:(i for i in g if f(i))))), [Generator, callable], 'filterfalse'],
    [getattr(itertools, 'izip', zip), [Generator, int], 'zip']
])

# aliases for better tab completion discovery
Generator.parallel_map = Generator.map_parallel
Generator.multicore_map = Generator.map_multicore
Generator.multithread_map = Generator.map_multithread

if __name__ == '__main__':

    g = Generator('hello')
    print(g)
    print(g.all_subslices().map(print, print).alternate('wwww', 'tttt').to(list))
    print(Generator(range(10)).map(print).to(list))
    print(Generator(range(10))[8])
    print(Generator(range(10))[-8])
    print(Generator(range(10))[1:5].to(list))
    print(Generator(range(10))[4:].to(list))
    print(Generator(range(10))[:4].to(list))
    print(Generator(range(10))[-5:-1].to(list))
    print(Generator(range(10))[-4:].to(list))
    print(Generator(range(10))[:-4].to(list))
    print(Generator(range(10))[1:5:2].to(list))
    print(Generator(range(10))[4::2].to(list))
    print(Generator(range(10))[:4:2].to(list))
    print(Generator(range(10))[1,5,2].to(list))
    print(Generator(range(10))[4,2].to(list))
    print(Generator(range(10))[2,4].to(list))
    print(Generator(range(10))[-1,-5,-2].to(list))
    print(Generator(range(10))[-4,-2].to(list))
    print(Generator(range(10))[-2,-4].to(list))
    print(Generator(range(10))[-2,-4].max())
    print(Generator(range(10))[-2,-4].min())
    print(Generator(range(10)).print()[-2,-4].print().sum())
    print(Generator(range(10)).print(end='\n-\n').consume())
    print(Generator(range(10)).print(end='\n--\n').run())
