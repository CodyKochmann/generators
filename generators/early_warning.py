from logging import warning

def early_warning(iterable):
    nxt = None
    prev = next(iterable)
    while 1:
        try:
            nxt = next(iterable)
        except:
            warning('this generator is now empty')
            yield prev
            break
        else:
            yield prev
            prev = nxt

if __name__ == '__main__':
    g = (i for i in range(5))
    g = early_warning(g)
    for i in range(5):
        print(next(g))

