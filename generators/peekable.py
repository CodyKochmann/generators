from functools import partial

class PeekableIterator(object):
    ''' Wrapping a generator with this provides a
        peek() function that lets you see whats coming
        on the next iteration. If the wrapped
        generator is done, calling peek() will return:

            <class 'StopIteration'>

        so you can control flow without needing to
        write code that relies on raised exceptions.
    '''
    def __init__(self, pipe):
        self.pipe=iter(pipe)
        self.preview=None
        self.steps=-2
        self._started=False
        self._next=partial(
            next,
            self.pipe,
            StopIteration
        )

    def peek(self):
        return self.preview

    def _first_step(self):
        self._started=True
        # Since self.preview is returned in _step
        # _step needs to be ran twice the first time.
        #
        # This is not done in __init__ because
        # iterators are lazy and do not manipulate
        # input pipes until their first iteration.
        return self._step()

    def _step(self, _input=None):
        self.steps+=1
        if self._started:
            prev = self.preview
            self.preview = self._next()
            return prev
        else:
            self._first_step()

    __next__, next, send = _step, _step, _step

    def __iter__(self):
        return iter(self._step, StopIteration)

    def __str__(self):
        return '<PeekableIterator steps={} next={}>'.format(*((
            self.steps, repr(self.preview)
        ) if self._started else (
            0, 'NotStarted'
        )))
    __repr__=__str__

def peekable(pipe):
    return PeekableIterator(pipe)

if __name__ == '__main__':
    g=(i for i in range(1,10))
    g=peekable(g)

    print(next(g))
    print(next(g))
    print(g.peek())
    print(next(g))
    for i in g:
        print('i -',i)
        print('preview -',g.peek())
        print(g)
    print(peekable(range(1)))

    print('---')
