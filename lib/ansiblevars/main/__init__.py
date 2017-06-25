import sys
import errno

from ansiblevars.project import Project


def main():
    path = "/Users/eric/dev/ansible/ansible-hydra"
    project = Project(path)
    for playbook in project.get_playbooks():
        report("Playbook", playbook.get_name(), playbook)
    for role in project.get_roles():
        report("Role", role.get_role_name(), role)


def report(tag, name, book):
    print("%s %s:" % (tag, name))
    for dx in book.get_defaults():
        print("   %s" % dx)
    for rx in book.get_references():
        print("   %s" % rx)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except IOError as exc:
        if exc.errno != errno.EPIPE:
            raise
    except RuntimeError as e:
        raise SystemExit(str(e))
