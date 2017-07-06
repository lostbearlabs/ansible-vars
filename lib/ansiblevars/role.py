# Represents a role

from ansiblevars.project_file import ProjectFile
import os


class Role(object):
    def __init__(self, role_name, path):
        self.role_name = role_name
        self.files = []
        self.path = path
        if path is not None:
            self.read_children(path)

    def read_children(self, path):
        for f in os.listdir(path):
            file_name, file_extension = os.path.splitext(f)
            full_path = os.path.join(path, f)
            if os.path.isfile(full_path) and file_extension == ".yml":
                child_file = ProjectFile(full_path)
                self.add_file(child_file)
            elif os.path.isdir(full_path):
                self.read_children(full_path)

    def get_role_name(self):
        return self.role_name

    def add_file(self, project_file):
        self.files.append(project_file)

    def get_references(self):
        refs = set()
        for f in self.files:
            refs.update(f.get_references())
        return refs

    def get_defaults(self):
        defs = set()
        for f in self.files:
            defs.update(f.get_defaults())
        return defs

