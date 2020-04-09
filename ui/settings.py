import json
from ui import qtx


class Settings:
    '''Class that looks like a normal dictionary, but is persistent.

        The persistence is backed by registry via QSettings service.

        Attention: known deviations from normal dict behavior:
            * saving tuples will return a list.
    '''

    def __init__(self, app_identity):
        '''Creates new persistent settings object for the application.

        '''
        self._engine = qtx.QSettings('innodata.com', app_identity)

    def get(self, key, default=None):
        if key in self:
            return _from_string(self._engine.value(key))
        return default

    def setdefault(self, key, default=None):
        if key not in self:
            self[key] = default
        return self[key]

    def clear(self):
        self._engine.clear()

    def keys(self):
        return self._engine.allKeys()

    def values(self):
        return [self[key] for key in self.keys()]

    def items(self):
        return zip(self.keys(), self.values())

    def update(self, *av, **kav):
        if av:
            if kav:
                raise ValueError('use only keyword arguments or only positional argument, not both')
            if len(av) != 1:
                raise ValueError('only one positional argument is expected')
            items = av[0]
            if type(items) is dict:
                items = items.items()
        else:
            items = kav.items()
        for k, v in items:
            self[k] = v

    def __getitem__(self, key):
        if key not in self:
            raise KeyError(key)

        return self.get(key)

    def __setitem__(self, key, value):
        if type(key) is not str or not key:
            raise ValueError('invalid key - must be non-empty string')

        self._engine.setValue(key, _as_string(value))

    def __delitem__(self, key):
        if key not in self:
            raise KeyError(key)

        self._engine.remove(key)

    def __contains__(self, key):
        return self._engine.contains(key)

    def __iter__(self):
        return iter(self.keys())


def _as_string(obj):
    if obj is None or type(obj) in (int, bytes):
        return obj
    return json.dumps(obj)

def _from_string(obj):
    if obj is None or type(obj) in (int, bytes):
        return obj
    return json.loads(obj)
