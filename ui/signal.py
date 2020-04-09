import functools

class Signal:
    '''Signal - similar to Qt signal, but in pure Python'''
    def __init__(self, *av):
        self._observers = {}
        self._id = 0

    def connect(self, target):
        if target is None:
            raise ValueError('can only connect to callable functions and methods')

        id_ = self._id
        self._id += 1
        self._observers[id_] = target

        return functools.partial(self._disconnect, id_)

    def _disconnect(self, target_id):
        self._observers.pop(target_id, None)

    def clear(self):
        self._observers.clear()
        self._id = 0

    def __call__(self, *av, **kav):
        for o in self._observers.values():
            o(*av, **kav)

    def emit(self, *av, **kav):
        self(*av, **kav)
