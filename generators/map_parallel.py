from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
from queue import Queue

from chunks import chunks

__all__ = 'map_parallel', 'map_multicore', 'map_multithread'

def _pool_map_stream(pool_type, pipe, fn, workers):
    assert callable(fn), fn
    assert isinstance(workers, int), workers
    assert workers > 0, workers
    p = pool_type(workers)
    job_q = Queue(maxsize=int(workers*2))
    try:
        for chunk in chunks(pipe, workers*2):
            for i in chunk:
                job_q.put(p.apply_async(fn, [i]))
            for i in pipe:
                yield job_q.get().get()
                job_q.put(p.apply_async(fn, [i]))
            while not job_q.empty():
                yield job_q.get().get()
    finally:
        p.terminate()

def map_multicore(pipe, fn, workers):
    ''' This streams map operations through a Pool without needing to load
        the entire stream into a massive list first, like Pool.map normally
        requires.
    '''
    assert callable(fn), fn
    assert isinstance(workers, int), workers
    assert workers > 0, workers
    pipe = iter(pipe)
    return _pool_map_stream(Pool, **locals())

def map_multithread(pipe, fn, workers):
    ''' This streams map operations through a ThreadPool without needing to
        load the entire stream into a massive list first, like ThreadPool.map
        normally requires.
    '''
    assert callable(fn), fn
    assert isinstance(workers, int), workers
    assert workers > 0, workers
    pipe = iter(pipe)
    return _pool_map_stream(ThreadPool, **locals())

def map_parallel(pipe, fn, workers):
    ''' This streams map operations in parallel through a pool of processes or
        threads. If the os does not allow multiprocessing or the datatypes are
        not serializable, operation reverts to ThreadPools
    '''
    assert callable(fn), fn
    assert isinstance(workers, int), workers
    assert workers > 0, workers
    pipe = iter(pipe)
    try:
        for i in map_multicore(pipe, fn, workers):
            yield i
    except:
        for i in map_multithread(pipe, fn, workers):
            yield i


if __name__ == '__main__':
    import random, time
    def work(i):
        print('working on: {}'.format(i))
        time.sleep(random.random())
        print('finished: {}'.format(i))
        return i*2
    l = G(
        range(10)
    ).map(
        float
    ).map_parallel(
        work,
        5
    ).print().run()
