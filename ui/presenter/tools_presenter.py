class ToolsPresenter:

    def __init__(self, bus, tools_menu, dialogs):
        self._bus = bus
        self._menu = tools_menu
        self._dialogs = dialogs

        self._project = None

        self._menu.metaRequested.connect(self._onMetaRequested)

        self._bus.projectOpened.connect(self._onProjectOpened)
        self._bus.projectClosed.connect(self._onProjectClosed)
        self._menu.setEnabled(False)

    def _onProjectOpened(self, project):
        self._project = project
        self._menu.setEnabled(True)

    def _onProjectClosed(self):
        self._menu.setEnabled(False)
        self._project = None

    def _onMetaRequested(self):
        if self._project is not None:
            for key, value in self._project.doc.meta.items():
                print(key, ':', value)