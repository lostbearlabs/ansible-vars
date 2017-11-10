import unittest

from ansiblevars.role import Role
from ansiblevars.project_file import ProjectFile
from ansiblevars.variable_default import VariableDefault
import os


class TestRole(unittest.TestCase):
    def test_getRoleName_constructedWithName_returnsIt(self):
        name = "123abc"
        sut = Role(name, None, None)
        self.assertEqual(name, sut.get_role_name())

    def test_getReferences_twoProjectFiles_mergesThem(self):
        p1 = ProjectFile(None, None)
        p1.add_reference('A')
        p1.add_reference('B')
        p2 = ProjectFile(None, None)
        p2.add_reference('A')
        p2.add_reference('C')

        sut = Role("", None, None)
        sut.add_file(p1)
        sut.add_file(p2)

        names = set(map(lambda x: x.get_variable_name(), sut.get_references()))
        self.assertEquals(set(['A', 'B', 'C']), names)

    def test_getDefaults_twoProjectFiles_mergesThem(self):
        p1 = ProjectFile(None, None)
        p1.add_default('A', '1')
        p1.add_default('B', '2')
        p2 = ProjectFile(None, None)
        p2.add_default('A', '3')
        p2.add_default('C', '4')

        sut = Role("", None, None)
        sut.add_file(p1)
        sut.add_file(p2)

        r1 = VariableDefault('A', '1', None)
        r2 = VariableDefault('B', '2', None)
        r3 = VariableDefault('A', '3', None)
        r4 = VariableDefault('C', '4', None)

        self.assertEquals(set([r1, r2, r3, r4]), sut.get_defaults())

    def test_getReferences_referenceInYaml_findsIt(self):
        path = os.getcwd() + "/test/artifacts/roles/role1"
        sut = Role("role1", path, None)
        self.assertTrue('test_var_2' in map(lambda x: x.get_variable_name(), sut.get_references()))

    def test_getDefaults_defaultInRoleDefault_findsIt(self):
        path = os.getcwd() + "/test/artifacts/roles/role1"
        sut = Role("role1", path, None)
        defs = filter(lambda x: x.get_variable_name() == 'test_var_3', sut.get_defaults())
        self.assertTrue(len(defs) == 1)
        self.assertTrue(defs[0].get_default_value() == 'value3')

    def test_getDefaults_defaultInYamls_findsIt(self):
        path = os.getcwd() + "/test/artifacts/roles/role1"
        sut = Role("role1", path, None)
        defs = filter(lambda x: x.get_variable_name() == 'test_var_4', sut.get_defaults())
        self.assertTrue(len(defs) == 1)
        self.assertTrue(defs[0].get_default_value() == 'value4')


if __name__ == '__main__':
    unittest.main()
