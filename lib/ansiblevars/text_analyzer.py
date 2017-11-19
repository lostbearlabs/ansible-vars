import re


# Examines non-YAML text (probably from a J2 template file?) for
# variable references.
class TextAnalyzer(object):

    def __init__(self):
        self.references = set()

    def get_references(self):
        return self.references

    def add_text(self, text):
        refs = re.findall('{{\s+([^\s]+)\s+[^}]*}}', text)
        for ref in refs:
            self.references.add(ref)

        refs = re.findall('{% for [^\s]+ in ([^\s]+)\s+%}', text)
        for ref in refs:
            self.references.add(ref)


