import unittest

from ansiblevars.role import Role
from ansiblevars.project_file import ProjectFile
import os


class TestRole(unittest.TestCase):
    def test_getRoleName_constructedWithName_returnsIt(self):
        name = "123abc"
        sut = Role(name, None)
        self.assertEqual(name, sut.get_role_name())

    def test_getReferences_twoProjectFiles_mergesThem(self):
        p1 = ProjectFile(None)
        p1.add_reference('A')
        p1.add_reference('B')
        p2 = ProjectFile(None)
        p2.add_reference('A')
        p2.add_reference('C')

        sut = Role("", None)
        sut.add_file(p1)
        sut.add_file(p2)

        self.assertEquals(set(['A', 'B', 'C']), sut.get_references())

    def test_getDefaults_twoProjectFiles_mergesThem(self):
        p1 = ProjectFile(None)
        p1.add_default('A', '1')
        p1.add_default('B', '2')
        p2 = ProjectFile(None)
        p2.add_default('A', '3')
        p2.add_default('C', '4')

        sut = Role("", None)
        sut.add_file(p1)
        sut.add_file(p2)

        self.assertEquals({'A': '3', 'B': '2', 'C': '4'}, sut.get_defaults())

    def test_getReferences_referenceInYaml_findsIt(self):
        path = os.getcwd() + "/test/artifacts/roles/role1"
        sut = Role("role1", path)
        self.assertTrue('test_var_2' in sut.get_references())

    def test_getDefaults_defaultInRoleDefault_findsIt(self):
        path = os.getcwd() + "/test/artifacts/roles/role1"
        sut = Role("role1", path)
        defs = sut.get_defaults()
        self.assertTrue(defs.has_key('test_var_3'))
        self.assertTrue(defs['test_var_3'] == 'value3')

    def test_getDefaults_defaultInYamls_findsIt (self):
        path = os.getcwd() + "/test/artifacts/roles/role1"
        sut = Role("role1", path)
        defs = sut.get_defaults()
        self.assertTrue(defs.has_key('test_var_4'))
        self.assertTrue(defs['test_var_4'] == 'value4')

if __name__ == '__main__':
    unittest.main()
