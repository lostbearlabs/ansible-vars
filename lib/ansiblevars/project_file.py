# Any file that contains variable references.
# Could be a playbook, a task within a role, etc.

import os
import yaml
import re


class ProjectFile(object):
    def __init__(self, file):
        self.defaults = {}
        self.references = set()
        self.file = file
        if file is not None:
            file_name, file_extension = os.path.splitext(os.path.basename(file))
            self.name = file_name
            is_role_defaults = re.match('.*/roles/.*/defaults/main.yml$', file)
            #print('parsing', file, is_role_defaults)
            self.parse_file(is_role_defaults)

    def get_file(self):
        return self.file

    def get_name(self):
        return self.name

    def add_default(self, name, value):
        self.defaults[name] = value

    def get_defaults(self):
        return self.defaults

    def add_reference(self, name):
        self.references.add(name)

    def get_references(self):
        return set(self.references)

    def parse_file(self, is_role_defaults):
        with open(self.file, 'r') as stream:
            try:
                yaml_obj = yaml.load(stream)
                if is_role_defaults:
                    self.read_role_defaults(yaml_obj)
                else:
                    self.read_yaml(yaml_obj)
            except yaml.YAMLError as exc:
                print(exc)

    def read_yaml(self, obj):
        if isinstance(obj, dict):
            for val in obj.values():
                self.read_yaml(val)
        elif isinstance(obj, list):
            for val in obj:
                self.read_yaml(val)
        else:
            self.read_reference(str(obj))

    def read_reference(self, txt):
        m = re.search('{{\s+([^\s]+)\s+}}', txt)
        if m:
            for grp in m.groups():
                #print('found', grp)
                self.add_reference(grp)

    def read_role_defaults(self, obj):
        if isinstance(obj, dict):
            for key in obj.keys():
                #print('found role default', key, obj[key])
                self.add_default(key, obj[key])
