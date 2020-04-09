from ui import qtx
import triq
from ..event_bus import Signal
from types import SimpleNamespace


class MainView(qtx.QMainWindow):

    def __init__(self, app):
        super().__init__()
        self.setObjectName('MainView')
        self.app = app
        self.closeRequested = Signal(object)
        self.closing = Signal()

    def closeEvent(self, event):
        vetoable = SimpleNamespace(vetoed=False)
        self.closeRequested.emit(vetoable)
        if vetoable.vetoed:
            event.ignore()
            return

        event.accept()
        self.closing.emit()
        self.hide()

        if all(w.isHidden() for w in self.app.topLevelWidgets() if w.isWindow()):
            triq.exit()

    def exec_(self):
        triq.run(self.app)
