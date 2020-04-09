from ui import qtx


class SettingsPresenter:

    def __init__(self, mainView, settings):
        self._mainView = mainView
        self._settings = settings

        self._mainView.closing.connect(self._onClosing)

        state = self._settings.get('mainState')
        if state:
            self._mainView.restoreState(qtx.QByteArray(state))
        geom = self._settings.get('mainGeometry')
        if geom:
            self._mainView.restoreGeometry(qtx.QByteArray(geom))


    def _onClosing(self):
        self._settings['mainState'] = self._mainView.saveState().data()
        self._settings['mainGeometry'] = self._mainView.saveGeometry().data()
        self._settings.sync()

