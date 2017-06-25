import unittest

from ansiblevars.project_file import ProjectFile
from tempfile import TemporaryFile, NamedTemporaryFile
import os

class TestProjectFile(unittest.TestCase):

    def setUp(self):
        self.temp_file = NamedTemporaryFile()

    def test_getFile_constructedWithFile_returnsIt(self):
        sut = ProjectFile(self.temp_file.name)
        self.assertEqual(self.temp_file.name, sut.get_file())

    def test_getDefaults_hasOneDefault_returnsIt(self):
        sut = ProjectFile(None)
        sut.add_default('A', '1')
        self.assertEqual({'A': '1'}, sut.get_defaults())

    def test_getReferences_hasTwoReferences_returnsThem(self):
        sut = ProjectFile(None)
        sut.add_reference('A')
        sut.add_reference('B')
        self.assertEquals({'A', 'B'}, sut.get_references())

    def test_getReferences_referenceInYaml_findsIt(self):
        # TODO: not hardcode
        path = os.getcwd() + "/test/artifacts/playbook1.yml"
        sut = ProjectFile(path)
        self.assertTrue( 'test_var_1' in sut.get_references() )

if __name__ == '__main__':
    unittest.main()
