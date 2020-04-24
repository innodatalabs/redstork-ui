from ui import qtx
from ..event_bus import Signal
from ..strip_args import strip_args
from ..res import res


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

        def action(icon=None, shortcut=None, emitter=None, text=None):
            a = qtx.QAction()
            if text is not None:
                a.setText(text)
            if emitter is not None:
                a.triggered.connect(strip_args(emitter))
            if shortcut is not None:
                a.setShortcut(shortcut)
            if icon is not None:
                a.setIcon(qtx.QIcon(icon))
            self.addAction(a)
            self._actions.append(a)

        action(res('icons/sharp_arrow_back_black_48dp.png'), 'PgUp', self.prevPage.emit)
        action(res('icons/sharp_arrow_forward_black_48dp.png'), 'PgDown', self.nextPage.emit)

        action(res('icons/sharp_zoom_out_black_48dp.png'), 'Ctrl+-', self.scaleDown.emit)
        action(res('icons/sharp_zoom_in_black_48dp.png'), 'Ctrl++', self.scaleUp.emit)

        action(res('icons/sharp_rotate_left_black_48dp.png'), 'Ctrl+Shift+/', self.rotateLeft.emit)
        action(res('icons/sharp_rotate_right_black_48dp.png'), 'Ctrl+/', self.rotateRight.emit)
