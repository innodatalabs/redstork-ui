from types import SimpleNamespace
from redstork import Document


class ProjectController:

    def open(self, file_name):
        project = SimpleNamespace()
        project.doc = Document(file_name)

        return project
