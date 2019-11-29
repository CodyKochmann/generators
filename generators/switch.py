def switch(pipe, expression, mapping, default=None):
    ''' switch statement logic that can be applied to a generator
        arguments:
          pipe: the iterable pipe you plan on iterating through
          expression: a callable funtion to select which mapping to use
          mapping: a dictionary of flags and callable functions the data
            will be forwarded through
          default: a callable function to run the data through if the 
            item's flag does not match any of the specified mappings
    '''
    assert callable(expression), expression
    assert isinstance(mapping, dict), mapping
    assert mapping, mapping
    assert all(callable(i) for i in mapping.values()), mapping
    assert callable(default) or default is None, default
    
    if default is None:
        for i in pipe:
            e = expression(i)
            yield mapping[e](i) if e in mapping else i
    else:
        for i in pipe:
            e = expression(i)
            yield mapping[e](i) if e in mapping else default(i)
