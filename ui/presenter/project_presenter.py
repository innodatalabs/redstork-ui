from types import SimpleNamespace


class ProjectPresenter:

    def __init__(self, bus, fileMenu, controller, dialogs, settings):
        self._bus = bus
        self._fileMenu = fileMenu
        self._controller = controller
        self._dialogs = dialogs
        self._settings = settings

        self._project = None

        recentlyOpened = self._settings.get('recentlyOpened', [])
        self._fileMenu.setRecentlyOpened(recentlyOpened)
        self._fileMenu.openRequested.connect(self._onOpenRequested)
        self._fileMenu.openRecentRequested.connect(self._onOpenFileRequested)
        self._fileMenu.closeRequested.connect(self._onCloseRequested)

    def _onOpenRequested(self):
        if self._project is not None:
            self._onCloseRequested()

        recentlyOpened = self._settings.get('recentlyOpened', [])
        defaultFilename = '' if not recentlyOpened else recentlyOpened[-1]
        file_name = self._dialogs.open_file(defaultFilename, '*.pdf', title='Open PDF file')
        if file_name is None:
            return

        if file_name in recentlyOpened:
            recentlyOpened.remove(file_name)
        recentlyOpened.append(file_name)
        if len(recentlyOpened) > 10:
            recentlyOpened.pop(0)
        self._settings['recentlyOpened'] = recentlyOpened

        self._project = self._controller.open(file_name)
        self._bus.projectOpened(self._project)

    def _onOpenFileRequested(self, filename):
        if self._project is not None:
            self._onCloseRequested()

        self._project = self._controller.open(file_name)
        self._bus.projectOpened(self._project)

    def _onCloseRequested(self):
        if self._project is None:
            return
        self._project = None
        self._bus.projectClosed.emit()
