from ui import qtx
from ..event_bus import Signal
from ..strip_args import strip_args


class Toolbar(qtx.QToolBar):

    def __init__(self, mainView):
        super().__init__(mainView)
        self.setObjectName('ToolBar')
        mainView.addToolBar(self)

        self.nextPage = Signal()
        self.prevPage = Signal()

        self.scaleUp = Signal()
        self.scaleDown = Signal()

        self.rotateRight = Signal()
        self.rotateLeft = Signal()

        self._actions = []

        def action(text, shortcut, emitter):
            a = qtx.QAction(text)
            a.triggered.connect(strip_args(emitter))
            if shortcut is not None:
                a.setShortcut(shortcut)
            self.addAction(a)
            self._actions.append(a)

        action('<', 'PgUp', self.prevPage.emit)
        action('>', 'PgDown', self.nextPage.emit)

        action('-', 'Ctrl+-', self.scaleDown.emit)
        action('+', 'Ctrl++', self.scaleUp.emit)

        action('/', 'Ctrl+/', self.rotateRight.emit)
        action('\\', 'Ctrl+Shift+/', self.rotateLeft.emit)
