import functools


def strip_args(f):
    '''
    Wraps a function that requires no arguments. The wrapper can be called with any
    arguments, positional or keyword - they all be ignored and wrapped function called
    without arguments.

    Useful when getting rid of unwanted parameters passed by a signal (e.g. PyQt5 QAction.triggered)
    '''
    @functools.wraps(f)
    def h(*av, **kav):
        return f()
    return h
