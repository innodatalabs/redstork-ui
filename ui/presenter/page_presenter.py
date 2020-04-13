import trio
import triq
from ui import qtx
from ..render import render
import tempfile
import os
import contextlib


class PdfPageModel:
    def __init__(self, pdf_name, page_index, crop_box, rotation, pool):
        self._pdf_name = pdf_name
        self._page_index = page_index
        self._crop_box = crop_box
        self._rotation = rotation
        self._pool = pool

    def crop_box(self):
        return self._crop_box

    def transform(self):
        transform = qtx.QTransform()
        transform = transform.rotate(90 * self._rotation)
        return transform

    async def render_at(self, scale):
        with temp_file_name_with_auto_remove(suffix='.ppm') as name:
            await render(self._pool, self._pdf_name, self._page_index, name, scale)
            image =  qtx.QImage(name)
            image = desaturate_image(image)
            return image


class PageModels:
    def __init__(self, doc, pool):
        self._doc = doc
        self._pool = pool

    def __getitem__(self, page_index):
        page = self._doc[page_index]
        crop_box = page.crop_box
        # if page.rotation in (1,3):
        #     crop_box = crop_box[1], crop_box[0], crop_box[3], crop_box[2]
        pdf_name = self._doc.file_name

        return PdfPageModel(pdf_name, page_index, crop_box, page.rotation, self._pool)

def desaturate_image(image):

    image = image.convertToFormat(
        qtx.QImage.Format_Indexed8,
        qtx.Qt.ImageConversionFlags(qtx.Qt.ThresholdDither)
    )

    def desaturate_color(color):
        r = (color >> 16) & 0xff
        g = (color >> 8) & 0xff
        b = color & 0xff
        gray = min(255, int(r * 0.30 + g * 0.59 + b * 0.11))  # luminocity of each color
        r = g = b = gray
        return 0xff000000 | (r << 16) | (g << 8) | b

    ctable = image.colorTable()
    ctable = [desaturate_color(c) for c in ctable]
    image.setColorTable(ctable)

    return image


class PagePresenter:
    def __init__(self, bus, view, toolbar, controller, pool):
        self._bus = bus
        self._view = view
        self._toolbar = toolbar
        self._controller = controller
        self._pool = pool

        self._currentPage = 1
        self._scale = 1.
        self._rotation = 0
        self._project = None

        self._toolbar.nextPage.connect(self._onNextPage)
        self._toolbar.prevPage.connect(self._onPrevPage)
        self._toolbar.scaleUp.connect(self._onScaleUp)
        self._toolbar.scaleDown.connect(self._onScaleDown)
        self._toolbar.rotateRight.connect(self._onRotateRight)
        self._toolbar.rotateLeft.connect(self._onRotateLeft)

        self._bus.projectOpened.connect(self._onProjectOpened)
        self._bus.projectClosed.connect(self._onProjectClosed)

    def _onProjectOpened(self, project):
        self._project = project
        self._page_models = PageModels(self._project.doc, self._pool)
        self._view.setEnabled(True)
        self._toolbar.setEnabled(True)
        self._currentPage = 1
        self._scale = 1.
        self._rotation = 0
        self._view.model = self._page_models[self._currentPage-1]

    def _onProjectClosed(self):
        self._view.setEnabled(False)
        self._toolbar.setEnabled(False)
        self._view.model = None
        self._project = None
        self._currentPage = 1
        self._scale = 1.
        self._rotation = 0

    def _onNextPage(self):
        if self._project is not None and self._currentPage < len(self._project.doc):
            self._currentPage += 1
            self._view.model = self._page_models[self._currentPage-1]
            self._bus.currentPageChanged.emit(self._currentPage)

    def _onPrevPage(self):
        if self._project is not None and self._currentPage > 1:
            self._currentPage -= 1
            self._view.model = self._page_models[self._currentPage-1]
            self._bus.currentPageChanged.emit(self._currentPage)

    def _onScaleUp(self):
        if self._project is not None:
            self._scale *= 1.2
            self._view.scale = self._scale

    def _onScaleDown(self):
        if self._project is not None:
            self._scale /= 1.2
            self._view.scale = self._scale

    def _onRotateRight(self):
        if self._project is not None:
            self._rotation = (self._rotation + 1) % 4
            self._view.rotation = self._rotation

    def _onRotateLeft(self):
        if self._project is not None:
            self._rotation = (self._rotation + 3) % 4
            self._view.rotation = self._rotation


@contextlib.contextmanager
def temp_file_name_with_auto_remove(prefix='', suffix=''):
    dir_ = tempfile.gettempdir()
    name = os.path.join(dir_, prefix + os.urandom(32).hex() + suffix)
    try:
        yield name
    finally:
        os.unlink(name)
