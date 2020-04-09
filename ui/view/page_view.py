from ui import qtx
from .page_scene_view import PageSceneView


class PageView(PageSceneView):
    def __init__(self):
        super().__init__(upside_down=True)  # we are in PDF coord system!
