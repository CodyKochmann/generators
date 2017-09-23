from __future__ import print_function

_print = print

def print(*a):
    try:
        _print(*a)
        return a[0] if len(a) == 1 else a
    except:
        _print(*a)



if __name__ == '__main__':
    g = (i for i in range(30))
    g = (print(i+1) if i%2 else i-1 for i in g)
    g = (sum((i,i)) for i in g)

    print(list(g))
