from collections import deque
from operator import itemgetter as og_itemgetter
from strict_functions import strict_globals

@strict_globals(deque=deque, itemgetter=og_itemgetter)
def itemgetter(iterable, indexes):
    ''' same functionality as operator.itemgetter except, this one supports
        both positive and negative indexing of generators as well '''
    indexes = indexes if isinstance(indexes, tuple) else tuple(indexes)
    assert all(isinstance(i, int) for i in indexes), 'indexes needs to be a tuple of ints'
    positive_indexes=[i for i in indexes if i>=0]
    negative_indexes=[i for i in indexes if i<0]
    out = {}
    if len(negative_indexes):
        # if there are any negative indexes
        negative_index_buffer = deque(maxlen=min(indexes)*-1)
        for i,x in enumerate(iterable):
            if i in positive_indexes:
                out[i]=x
            negative_index_buffer.append(x)
        out.update({ni:negative_index_buffer[ni] for ni in negative_indexes})
    else:
        # if just positive results
        out.update({i:x for i,x in enumerate(iterable) if i in positive_indexes})
    return itemgetter(*indexes)(out)

del deque, strict_globals, og_itemgetter

if __name__ == '__main__':
    print(itemgetter(range(20), (-2, 2, 4, 6, -5, -10, -1)))

