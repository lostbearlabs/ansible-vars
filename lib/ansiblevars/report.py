
class Report(object):

    def __init__(self, project):
        self.playbooks = project.get_playbooks()
        self.roles = project.get_roles()

        self.all_references = set()
        self.all_defaults = set()
        for playbook in self.playbooks:
            self.all_references.update(playbook.get_references())
            self.all_defaults.update(playbook.get_defaults())
        for role in self.roles:
            self.all_references.update(role.get_references())
            self.all_defaults.update(role.get_defaults())

    def display(self):

        self.header("Playbooks")
        for playbook in sorted(self.playbooks, key=lambda p: p.get_name()):
            self.display_summary("Playbook", playbook.get_name(), playbook)

        self.header("Roles")
        for role in sorted(self.roles, key=lambda r: r.get_role_name()):
            self.display_summary("Role", role.get_role_name(), role)

        self.header("Set but never referenced")
        self.display_set_unreferenced()

        self.header("Referenced but never set")
        self.display_referenced_unset()

        self.header("Different defaults for same variable")
        self.different_defaults_same_variable()

        self.header("Same default set in multiple places")
        self.same_default_multiple_places()

        print("... done")

    def same_default_multiple_places(self):
        defs = {}
        for dx in self.all_defaults:
            value = dx.get_default_value()
            if value not in defs:
                defs[value] = set()
            defs[value].add(dx)

        n = 0
        for key in sorted(defs.keys()):
            defaults = defs[key]
            if len(defaults) > 1:
                n += 1
                print("      default value '%s' found in:" % key)
                for dx in defaults:
                    print("         %s" % dx)
        if n == 0:
            print("      (none found)")

    def different_defaults_same_variable(self):
        defs = {}
        for dx in self.all_defaults:
            name = dx.get_variable_name()
            if name not in defs:
                defs[name] = set()
            defs[name].add(dx)

        n = 0
        for key in sorted(defs.keys()):
            vals = set()
            for val in defs[key]:
                vals.add( val.get_default_value() )
            if len(vals) > 1:
                n = n + 1
                print("      different defaults for %s" % key)
                for dx in defs[key]:
                    print("         %s" % dx)

        if n == 0:
            print("      (none found)")

    def display_set_unreferenced(self):
        names_referenced = set()
        for rx in self.all_references:
            names_referenced.add(rx.get_variable_name())

        n = 0
        for dx in sorted( self.all_defaults, key=lambda x: x.get_variable_name()):
            if not dx.get_variable_name() in names_referenced:
                print("   %s" % dx)
                n += 1
        if n == 0:
            print('   (none found)')

    def display_referenced_unset(self):
        names_set = set()
        for dx in self.all_defaults:
            names_set.add(dx.get_variable_name())

        n = 0
        for rx in sorted( self.all_references, key=lambda x: x.get_variable_name()):
            if not rx.get_variable_name() in names_set:
                print("   %s" % rx)
                n += 1
        if n == 0:
            print('   (none found)')

    def display_summary(self, tag, name, book):
        print("%s %s:" % (tag, name))
        print("   defaults:")
        defaults = book.get_defaults();
        if defaults:
            for dx in sorted(defaults, key=lambda p: p.get_variable_name()):
                print("      %s" % dx)
        references = book.get_references()
        print("   references:")
        if references:
            for rx in sorted(references, key=lambda p: p.get_variable_name()):
                print("      %s" % rx)

    def header(self, text):
        print
        print('======================')
        print(text)
        print('======================')

