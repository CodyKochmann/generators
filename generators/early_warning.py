from logging import warning
from strict_functions import strict_globals


@strict_globals(warning=warning)
def early_warning(iterable, name='this generator'):
    ''' This function logs an early warning that the generator is empty.

    This is handy for times when you're manually playing with generators and
    would appreciate the console warning you ahead of time that your generator
    is now empty, instead of being surprised with a StopIteration or
    GeneratorExit exception when youre trying to test something. '''

    nxt = None
    prev = next(iterable)
    while 1:
        try:
            nxt = next(iterable)
        except:
            warning(' {} is now empty'.format(name))
            yield prev
            break
        else:
            yield prev
            prev = nxt


del warning
del strict_globals


if __name__ == '__main__':
    g = (i for i in range(5))
    g = early_warning(g, 'range_of_5')
    for i in range(5):
        print(next(g))

