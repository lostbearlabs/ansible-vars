import sys
import errno

from ansiblevars.project import Project


def main():
    path = "/Users/eric/dev/ansible/ansible-hydra"
    project = Project(path)
    for playbook in sorted(project.get_playbooks(), key=lambda p: p.get_name()):
        report("Playbook", playbook.get_name(), playbook)
    for role in sorted(project.get_roles(), key=lambda r: r.get_role_name()):
        report("Role", role.get_role_name(), role)


def report(tag, name, book):
    print("%s %s:" % (tag, name))
    print("   defaults:")
    defaults = book.get_defaults();
    if defaults:
        for key in sorted(defaults.keys()):
            print("      %s ==> %s" % (key, defaults[key]))
    references = book.get_references()
    print("   references:")
    if references:
        for rx in sorted(references):
            print("      %s" % rx)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except IOError as exc:
        if exc.errno != errno.EPIPE:
            raise
    except RuntimeError as e:
        raise SystemExit(str(e))
