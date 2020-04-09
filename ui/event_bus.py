from .signal import Signal


class EventBus:
    '''Event bus.'''

    def __init__(self):
        self._signals = {}

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        return self[name]

    def __getitem__(self, name):
        if name not in self._signals:
            self._signals[name] = Signal()
        return self._signals[name]
