from redstork import PageObject


class AnnotController:
    def get_annotations(self, project, page_index):
        page = project.doc[page_index]

        yield from page.flat_iter()


