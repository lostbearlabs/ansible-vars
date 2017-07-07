import unittest
import os
from ansiblevars.project import Project

class TestProject(unittest.TestCase):

    def setUp(self):
        path = os.getcwd() + "/test/artifacts"
        self.sut = Project(path, None)

    def test_getPlaybooks_includesPlaybook1(self):
        name = "playbook1"
        playbook = self.sut.get_playbook(name)
        self.assertIsNotNone(playbook)
        self.assertEqual(name, playbook.get_name())

    def test_getRoles_includesRole1(self):
        name = "role1"
        role = self.sut.get_role(name)
        self.assertIsNotNone(role)
        self.assertEqual(name, role.get_role_name())


if __name__ == '__main__':
    unittest.main()
