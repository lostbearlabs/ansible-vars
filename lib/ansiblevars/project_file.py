# Any file that contains variable references.
# Could be a playbook, a task within a role, etc.

import os
import yaml
import re
from ansiblevars.variable_reference import VariableReference
from ansiblevars.variable_default import VariableDefault
from ansiblevars.text_analyzer import TextAnalyzer


class ProjectFile(object):
    def __init__(self, file, config):
        self.defaults = set()
        self.references = set()
        self.file = file
        self.config = config
        if self.file is not None:
            file_name, file_extension = os.path.splitext(os.path.basename(file))
            self.name = file_name

    def parse_from_yaml(self):
        if self.file is not None:
            is_role_defaults = re.match('.*/roles/.*/defaults/main.yml$', self.file)
            self.parse_file(is_role_defaults)

    def parse_from_text(self):
        if self.file is not None:
            self.trace("parse_from_j2 file=%s" % self.file)
            with open(self.file, 'r') as stream:
                text = stream.read()
                analyzer = TextAnalyzer()
                analyzer.add_text(text)
                for ref in analyzer.get_references():
                    self.add_reference(ref)

    def verbose(self):
        return self.config is not None and self.config.is_verbose()

    def trace(self, msg):
        if self.verbose():
            print(msg)

    def get_file(self):
        return self.file

    def get_name(self):
        return self.name

    def add_default(self, name, value):
        self.defaults.add(VariableDefault(name, str(value), self.file))

    def get_defaults(self):
        return self.defaults

    def add_reference(self, name):
        self.references.add(VariableReference(name, self.file))

    def get_references(self):
        return set(self.references)

    def parse_file(self, is_role_defaults):
        self.trace("parse_file file=%s, is_role_defaults=%s" % (self.file, is_role_defaults))
        with open(self.file, 'r') as stream:
            try:
                yaml_obj = yaml.load(stream)
                if is_role_defaults:
                    self.read_defaults(yaml_obj, "  ")
                else:
                    self.read_yaml(yaml_obj, "  ")
            except yaml.YAMLError as exc:
                print(exc)

    # TODO: for yml files, need to detect reference to yyy in:
    #    when: yyy
    #    when: not yyy
    #    etc
    def read_yaml(self, obj, indent):
        self.trace("%stype=%s" % (indent, type(obj)))
        if isinstance(obj, dict):
            self.trace("%sfound dictionary" % indent)
            for key in obj.keys():
                val = obj[key]
                self.trace("%s process key %s" % (indent, key))
                if key == 'vars':
                    # print('FOUND VARS', val)
                    self.read_defaults(val, indent)
                else:
                    self.read_yaml(val, indent + "  ")
        elif isinstance(obj, list):
            self.trace("%sfound list" % indent)
            for val in obj:
                self.read_yaml(val, indent + "  ")
        else:
            self.trace("%sfound scalar: %s" % (indent, str(obj)))
            self.read_reference(str(obj), indent)


    def read_reference(self, txt, indent):
        refs = re.findall('{{\s+([^\s]+)\s+[^}]*}}', txt)
        for ref in refs:
            self.trace("%s   found reference: %s" % (indent, ref))
            self.add_reference(ref)

    def read_defaults(self, obj, indent):
        if isinstance(obj, dict):
            for key in obj.keys():
                self.trace("%s   found default: %s => %s" % (indent, key, obj[key]))
                self.add_default(key, obj[key])
                # the default may be reading from another var
                self.read_reference(str(obj[key]), indent)
