from ui import qtx
from ..event_bus import Signal
from ..strip_args import strip_args


class FileMenu:

    def setRecentlyOpened(self, values):
        pass

    def __init__(self, mainView):

        self.openRequested = Signal()
        self.openRecentRequested = Signal(str)
        self.saveRequested = Signal()
        self.saveAsRequested = Signal()
        self.closeRequested = Signal()

        menubar = mainView.menuBar()
        self._fileMenu = menubar.addMenu('&File')

        openAction = qtx.QAction('&Open', mainView)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open PDF file')
        openAction.triggered.connect(strip_args(self.openRequested))
        self._fileMenu.addAction(openAction)

        saveAction = qtx.QAction('&Save', mainView)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save')
        saveAction.triggered.connect(strip_args(self.saveRequested))
        self._fileMenu.addAction(saveAction)

        closeAction = qtx.QAction('&Close', mainView)
        closeAction.setShortcut('Ctrl+C')
        closeAction.setStatusTip('Close')
        closeAction.triggered.connect(strip_args(self.closeRequested))
        self._fileMenu.addAction(closeAction)

        self._fileMenu.addSeparator()

        exitAction = qtx.QAction('&Exit', mainView)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(mainView.close)
        self._fileMenu.addAction(exitAction)

