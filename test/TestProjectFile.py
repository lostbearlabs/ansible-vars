import unittest

from ansiblevars.project_file import ProjectFile
from tempfile import TemporaryFile, NamedTemporaryFile
import os
from ansiblevars.variable_default import VariableDefault


class TestProjectFile(unittest.TestCase):
    def setUp(self):
        self.temp_file = NamedTemporaryFile()

    def test_getFile_constructedWithFile_returnsIt(self):
        sut = ProjectFile(self.temp_file.name, None)
        self.assertEqual(self.temp_file.name, sut.get_file())

    def test_getDefaults_hasOneDefault_returnsIt(self):
        sut = ProjectFile(None, None)
        sut.add_default('A', '1')
        self.assertEqual(set([VariableDefault('A', '1', None)]), sut.get_defaults())

    def test_getReferences_hasTwoReferences_returnsThem(self):
        sut = ProjectFile(None, None)
        sut.add_reference('A')
        sut.add_reference('B')
        self.assertEquals({'A', 'B'}, set(map(lambda x: x.get_variable_name(), sut.get_references())))

    def test_getReferences_referenceInYaml_findsIt(self):
        path = os.getcwd() + "/test/artifacts/playbook1.yml"
        sut = ProjectFile(path, None)
        sut.parse_from_yaml()
        self.assertTrue('test_var_1' in map(lambda x: x.get_variable_name(), sut.get_references()))


if __name__ == '__main__':
    unittest.main()
