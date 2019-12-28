import logging

def skip_errors(pipe, *, log=True, logger=None, ex_type=Exception):
    # validate types
    assert logger is None or isinstance(logger, logging.Logger), logger
    assert isinstance(log, bool), log
    assert issubclass(ex_type, BaseException), ex_type
    # organize parameters, cuz i suck at this
    logger_defined = logger is not None
    log = log or logger_defined
    if log:
        logger = logger if logger_defined else logging.root
    else:
        logger = None
    del logger_defined
    # validate options state
    assert (logger is not None and log == True) or (logger is None and log == False), [logger, log]
    # set up actual processor
    def processor(pipe):
        # now run everything
        running = True
        while running:
            running = False
            try:
                for i in pipe:
                    yield i
            except ex_type as e:
                running = True
                if log:
                    logger.exception(e)
    return processor(pipe)
