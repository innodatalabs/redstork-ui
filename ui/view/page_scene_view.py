from ui import qtx
from ..signal import Signal
import triq


class PageModel:
    '''
    Canvas with asyncronously rendered background image.

    View can scale and rotate the canvas. While rotation is just a simple image operation,
    scaling requires re-rendering to keep the sharpness. When scale factor changes,
    View will do fast background image scaling, and asynchronously request new image.
    '''

    async def render_at(self, scale):
        ''' asynchronously renders page to an image, and returns QPixmap '''
        pass

    def crop_box(self):
        pass

    def transform(self):
        pass


class DummyLetterPageModel(PageModel):
    def crop_box(self):
        return 0., 0., 612., 792.  # 8.5in x 11in - Letter size


class PageScene(qtx.QGraphicsScene):
    '''
    Graphics scene that allows one to set background pixmap (default implementation
    unfortunately draws it tiled).
    '''

    '''
    Signal emitted when area is marked using Ctrl key
    '''
    onControlMouseRelease = Signal(tuple)

    def __init__(self, *av, **kaw):
        super().__init__(*av, **kaw)
        self._bg_pixmap = None
        self._last_scene_pos = None

    @property
    def background_pixmap(self):
        return self._bg_pixmap

    @background_pixmap.setter
    def background_pixmap(self, pixmap):
        self._bg_pixmap = pixmap
        self.update()

    def drawBackground(self, painter, rect):
        sceneRect = self.sceneRect()
        painter.fillRect(rect, qtx.QBrush(qtx.Qt.lightGray))
        painter.setBrush(qtx.Qt.darkGray)
        painter.setPen(qtx.Qt.NoPen)
        # painter.drawRoundedRect(sceneRect.translated(4, -4), 2, 2)
        if self._bg_pixmap:
            painter.drawPixmap(sceneRect, self._bg_pixmap, qtx.QRectF(self._bg_pixmap.rect()))
        else:
            painter.fillRect(rect.intersected(sceneRect), qtx.QBrush(qtx.Qt.white))

        painter.setBrush(qtx.Qt.NoBrush)
        painter.setPen(qtx.QPen(qtx.Qt.darkGray, 0.75))

        painter.drawRect(sceneRect)

    def mouseReleaseEvent(self, event):
        if (qtx.Qt.ControlModifier & event.modifiers()) and self._last_scene_pos is not None:
            x0, y0 = self._last_scene_pos.x(), self._last_scene_pos.y()
            x1, y1 = event.scenePos().x(), event.scenePos().y()
            if x0 > x1:
                x0, x1 = x1, x0
            if y0 > y1:
                y0, y1 = y1, y0
            self.onControlMouseRelease.emit((x0, y0, x1, y1))
            self._last_scene_pos = None
        return qtx.QGraphicsScene.mouseReleaseEvent(self, event)

    def mousePressEvent(self, event):
        self._last_scene_pos = event.scenePos()
        return qtx.QGraphicsScene.mousePressEvent(self, event)


class PageSceneView(qtx.QGraphicsView):

    def __init__(self, *args, upside_down=False, **kargs):
        '''Creates a new PageView component.

        Args:
            upside_down (bool): coordinate system direction. Set to ``True`` to use PDF-style coordinate system with
                origin in the left **bottom** corner. Default is ``False``, corresponding to image-like coordinate
                system with origin in the left **top** corner, and growing down.
            args: passed to superclass as-is
            kargs: passed to superclass as-is
        '''
        super().__init__(*args, **kargs)

        self._scene = PageScene(parent=self)
        self.setScene(self._scene)
        self.scene().setItemIndexMethod(qtx.QGraphicsScene.NoIndex)
        self.setCacheMode(qtx.QGraphicsView.CacheBackground)
        self.setDragMode(qtx.QGraphicsView.RubberBandDrag)

        self.setRenderHint(qtx.QPainter.Antialiasing)
        #self.setRenderHint(QPainter.SmoothPixmapTransform)

        self._scale = 1.0
        self._rotation = 0
        self._upside_down = upside_down

        self._model = DummyLetterPageModel()
        self._bg_image = None

        self.scene().setSceneRect(*self._model.crop_box())
        self._set_current_transform()

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model):
        if model is None:
            model = DummyLetterPageModel()
        self._model = model
        self._scene.background_pixmap = None  # FIXME: do we need this, or let old page show until new one is ready? -MK
        x0, y0, x1, y1 = self._model.crop_box()
        self._scene.setSceneRect(x0, y0, x1-x0, y1-y0)
        top = 0
        if self._upside_down:
            top = y1-y0
        self.centerOn(qtx.QPointF( (x1 - x0) / 2., top))

        self._set_current_transform()
        triq.call_async(self._render_background_image)

    async def _render_background_image(self):
        image = await self.model.render_at(self._scale)
        if image is not None:
            if self._upside_down:
                image = image.mirrored(False, True)
            self._bgImage = qtx.QPixmap(image)
            self._scene.background_pixmap = self._bgImage
            self._set_current_transform()

    def _set_current_transform(self):
        transform = self._model.transform() or qtx.QTransform()
        transform.rotate(self._rotation * 90)
        y_scale = -self._scale if self._upside_down else self._scale
        transform.scale(self._scale, y_scale)
        self.setTransform(transform)
        self.resetCachedContent()

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
        self._set_current_transform()
        triq.call_async(self._render_background_image)

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        self._rotation = value % 4
        self._set_current_transform()
