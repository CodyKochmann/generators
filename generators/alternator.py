from itertools import cycle

def alternator(*pipes):
    ''' a lot like zip, just instead of:
            (a,b),(a,b),(a,b)
        it works more like:
            a,b,a,b,a,b,a
        until one of the pipes ends '''
    try:
        for p in cycle(map(iter, pipes)):
            yield next(p)
    except StopIteration:
        pass

if __name__ == '__main__':
    a=range(6)
    b=range(4)
    print(list(alternator(a,b)))
