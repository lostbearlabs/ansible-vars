import yaml
import re


# Examines a YAML text (from a playbook or role) for
# variable references and defaults.
class YamlAnalyzer(object):
    def __init__(self, config):
        self.references = set()
        self.defaults = dict()
        self.config = config

    def verbose(self):
        return self.config is not None and self.config.is_verbose()

    def trace(self, msg):
        if self.verbose():
            print(msg)

    def get_references(self):
        return self.references

    def get_defaults(self):
        return self.defaults

    def add_yaml(self, text, is_role_defaults):
        try:
            yaml_obj = yaml.load(text)
            if is_role_defaults:
                self.read_defaults(yaml_obj, "  ")
            else:
                self.read_yaml(yaml_obj, "  ")
        except yaml.YAMLError as exc:
            print(exc)

    def read_yaml(self, obj, indent):
        self.trace("%stype=%s" % (indent, type(obj)))
        if isinstance(obj, dict):
            self.trace("%sfound dictionary" % indent)
            for key,val in obj.iteritems():
                self.trace("%s process key %s" % (indent, key))
                if key == 'vars':
                    self.read_defaults(val, indent)
                elif key == 'when':
                    self.read_when(val, indent)
                else:
                    self.read_yaml(val, indent + "  ")
        elif isinstance(obj, list):
            self.trace("%sfound list" % indent)
            for val in obj:
                self.read_yaml(val, indent + "  ")
        else:
            self.trace("%sfound scalar: %s" % (indent, str(obj)))
            self.read_reference(str(obj), indent)

    def read_when(self, txt, indent):
        if isinstance(txt, list):
            for val in txt:
                self.read_when(val, indent)
        else:
            refs = re.findall('[A-Za-z0-9_]+', txt)
            # for now, just take the first legal identifier we can find
            for ref in refs:
                self.trace("%s   found when reference: %s" % (indent, ref))
                self.references.add(ref)
                break

    def read_reference(self, txt, indent):
        refs = re.findall('{{\s+([^\s]+)\s+[^}]*}}', txt)
        for ref in refs:
            self.trace("%s   found reference: %s" % (indent, ref))
            self.references.add(ref)

    def read_defaults(self, obj, indent):
        if isinstance(obj, dict):
            for key in obj.keys():
                self.trace("%s   found default: %s => %s" % (indent, key, obj[key]))
                self.defaults[key] = obj[key]
                # the default may be reading from another var
                self.read_reference(str(obj[key]), indent)
