import re

class TextAnalyzer(object):

    def __init__(self):
        self.references = set()

    def get_references(self):
        return self.references

    # TODO: for template files, need to detect reference to yyy in:
    #    {% for x in yyy %}

    def add_text(self, text):
        refs = re.findall('{{\s+([^\s]+)\s+[^}]*}}', text)
        for ref in refs:
            self.references.add(ref)

        refs = re.findall('{% for [^\s]+ in ([^\s]+)\s+%}', text)
        for ref in refs:
            self.references.add(ref)


