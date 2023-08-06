import functools


def chain(*funcs, initial_func=None):
    if initial_func:
        return functools.reduce(lambda prev, curr: (lambda x: curr(prev(x))), funcs, initial_func)
    else:
        return functools.reduce(lambda prev, curr: (lambda x: curr(prev(x))), funcs)
