import sys
import errno

from ansiblevars.project import Project
from ansiblevars.report import Report
from ansiblevars.config import Config
from optparse import OptionParser


def main():

    usage = "usage: ansible-vars [args]"
    parser = OptionParser()
    parser.add_option("-d", "--directory", action="store", type="string", dest="dir",
                      help="directory where ansible playbooks and roles are located")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="trace program execution")

    (options, args) = parser.parse_args()

    if options.dir is None:
        parser.print_usage()
        parser.print_usage()
        exit(1)

    config = Config(options.verbose)
    project = Project(options.dir, config)
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
