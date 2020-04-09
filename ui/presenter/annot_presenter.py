from ui import qtx


class AnnotPresenter:

    def __init__(self, bus, scene, controller):
        self._bus = bus
        self._scene = scene
        self._controller = controller

        self._project = None

        self._bus.projectOpened.connect(self._onProjectOpened)
        self._bus.projectClosed.connect(self._onProjectClosed)

        self._bus.currentPageChanged.connect(self._onCurrentPageChanged)

    def _onProjectOpened(self, project):
        self._project = project
        self._drawAnnot(0)  # draw page 0

    def _onProjectClosed(self):
        self._scene.clear()
        self._project = None

    def _onCurrentPageChanged(self, pageno):
        self._scene.clear()
        self._drawAnnot(pageno-1)

    def _drawAnnot(self, page_index):
        annots = self._controller.get_annotations(self._project, page_index)

        for a in annots:
            x0, y0, x1, y1 = a.rect
            item = qtx.QGraphicsRectItem(x0, y0, x1-x0, y1-y0)
            # item.setTransform(qtx.QTransform(*a.matrix).inverted()[0])

            penColor = qtx.Qt.gray
            if a.type == 1:
                penColor = qtx.Qt.green
            elif a.type == 2:
                penColor = qtx.Qt.red
            elif a.type == 3:
                penColor = qtx.Qt.blue
            item.setPen(qtx.QPen(penColor, 0.5))

            self._scene.addItem(item)
