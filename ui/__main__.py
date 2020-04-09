import multiprocessing
from .event_bus import EventBus
from .settings import Settings


with multiprocessing.Pool() as pool:
    from ui import qtx

    app = qtx.QApplication([])

    settings = Settings('redstork-sample')
    bus = EventBus()

    from .view.main_view import MainView
    mainView = MainView(app)
    from .dialogs import Dialogs
    dialogs = Dialogs(mainView)

    from .view.file_menu import FileMenu
    fileMenu = FileMenu(mainView)
    from .controller.project_controller import ProjectController
    projectController = ProjectController()
    from .presenter.project_presenter import ProjectPresenter
    project_presenter = ProjectPresenter(bus, fileMenu, projectController, dialogs, settings)

    from .view.toolbar import Toolbar
    toolbar = Toolbar(mainView)
    from .view.page_view import PageView
    pageView = PageView()
    mainView.setCentralWidget(pageView)
    from .presenter.page_presenter import PagePresenter
    pagePresenter = PagePresenter(bus, pageView, toolbar, None, pool)

    from .view.tools_menu import ToolsMenu
    toolsMenu = ToolsMenu(mainView)
    from .presenter.tools_presenter import ToolsPresenter
    toolsPresenter = ToolsPresenter(bus, toolsMenu, dialogs)

    from .controller.annot_controller import AnnotController
    annotController = AnnotController()
    from .presenter.annot_presenter import AnnotPresenter
    annotPresenter = AnnotPresenter(bus, pageView.scene(), annotController)

    from .presenter.settings_presenter import SettingsPresenter
    settingsPresenter = SettingsPresenter(mainView, settings)

    mainView.show()
    mainView.exec_()
