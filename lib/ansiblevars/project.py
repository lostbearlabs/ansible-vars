# Represents a project, containing both playbooks and roles

## TODO NEXT:  IMPLEMENT THIS!

# Testing idea:  let's just have a test project as an artifact under the tests folder and
# read its actual contents.  No point getting to unit-test-purist here.

import os
from os.path import basename

from ansiblevars.project_file import ProjectFile
from ansiblevars.role import Role


class Project(object):
    def __init__(self, path):
        self.playbooks = {}
        self.roles = {}
        self.find_playbooks(path)
        self.find_roles(path)

    def find_roles(self, path):
        path = os.path.join(path, 'roles')
        for f in os.listdir(path):
            file_name, file_extension = os.path.splitext(f)
            full_path = os.path.join(path, f)
            if os.path.isdir(full_path):
                b = basename(file_name)
                self.roles[b] = Role(b, full_path)

    def find_playbooks(self, path):
        for f in os.listdir(path):
            file_name, file_extension = os.path.splitext(f)
            full_path = os.path.join(path, f)
            if os.path.isfile(full_path) and file_extension == ".yml":
                b = basename(file_name)
                self.playbooks[b] = ProjectFile(full_path)

    def get_playbooks(self):
        return set(self.playbooks.values())

    def get_playbook(self, name):
        return self.playbooks[name]

    def get_roles(self):
        return set(self.roles.values())

    def get_role(self, role_name):
        role = self.roles[role_name]
        if role is None:
            role = Role(role_name)
            self.roles[role_name] = role
        return role
