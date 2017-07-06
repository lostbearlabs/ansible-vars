import sys
import errno

from ansiblevars.project import Project
from ansiblevars.report import Report


def main():
    path = "/Users/eric/dev/ansible/ansible-hydra"
    project = Project(path)
    report = Report(project)
    report.display()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except IOError as exc:
        if exc.errno != errno.EPIPE:
            raise
    except RuntimeError as e:
        raise SystemExit(str(e))
