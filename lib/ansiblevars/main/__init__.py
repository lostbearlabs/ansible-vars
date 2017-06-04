import sys
import errno

from ansiblevars.fnord import get_fnord


def main():
    print(get_fnord())


if __name__ == "__main__":
    try:
        sys.exit(main())
    except IOError as exc:
        if exc.errno != errno.EPIPE:
            raise
    except RuntimeError as e:
        raise SystemExit(str(e))
