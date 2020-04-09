from ui import qtx
from ..event_bus import Signal
from ..strip_args import strip_args


class ToolsMenu:

    def setEnabled(self, what):
        self._toolsMenu.setEnabled(what)

    def __init__(self, mainView):

        self.metaRequested = Signal()

        menubar = mainView.menuBar()
        self._toolsMenu = menubar.addMenu('&Tools')

        showMetaAction = qtx.QAction('&Info', mainView)
        showMetaAction.setStatusTip('Show PDF file info')
        showMetaAction.triggered.connect(strip_args(self.metaRequested))
        self._toolsMenu.addAction(showMetaAction)


