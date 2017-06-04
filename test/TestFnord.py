import unittest

from ansiblevars.fnord import get_fnord


class TestFnord(unittest.TestCase):

    def test_get_fnord(self):
        self.assertEqual("fnord", get_fnord())


if __name__ == '__main__':
    unittest.main()
