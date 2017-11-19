# Any file that contains variable references.
# Could be a playbook, a task within a role, etc.

import os
import re
from ansiblevars.variable_reference import VariableReference
from ansiblevars.variable_default import VariableDefault
from ansiblevars.text_analyzer import TextAnalyzer
from ansiblevars.yaml_analyzer import YamlAnalyzer


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
            with open(self.file, 'r') as stream:
                text = stream.read()
                analyzer = YamlAnalyzer(self.config)
                analyzer.add_yaml(text, is_role_defaults)
                for ref in analyzer.get_references():
                    self.add_reference(ref)
                for key,val in analyzer.get_defaults().iteritems():
                    self.add_default(key,val)

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


