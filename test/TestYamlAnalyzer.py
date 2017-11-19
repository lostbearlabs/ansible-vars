import unittest
from ansiblevars.yaml_analyzer import YamlAnalyzer


class TestYamlAnalyzer(unittest.TestCase):
    def setUp(self):
        self.sut = YamlAnalyzer(None)

    def test_simpleRef_findsIt(self):
        text = """
---
- test1: "{{ tree }}"
"""
        self.sut.add_yaml(text, False)
        expected = set(["tree"])
        self.assertSetEqual(self.sut.get_references(), expected)

    def test_refWithPipe_findsIt(self):
        text = """
---
- test1: "{{ tree | lower }}"
"""
        self.sut.add_yaml(text, False)
        expected = set(["tree"])
        self.assertSetEqual(self.sut.get_references(), expected)

    def test_twoRefs_findsBoth(self):
        text = """
---
- test1: aaa="{{ tree }}" bbb="{{ frog }}"
"""
        self.sut.add_yaml(text, False)
        expected = set(["tree", "frog"])
        self.assertSetEqual(self.sut.get_references(), expected)

    def test_simpleWhenRef_findsIt(self):
        text = """
---
- test1: "{{ tree }}"
  when: fnord
"""
        self.sut.add_yaml(text, False)
        expected = set(["tree", "fnord"])
        self.assertSetEqual(self.sut.get_references(), expected)

    def test_listWhenRef_findsIt(self):
        text = """
---
- test1: "{{ tree }}"
  when: [fnord]
"""
        self.sut.add_yaml(text, False)
        expected = set(["tree", "fnord"])
        self.assertSetEqual(self.sut.get_references(), expected)

    def test_expressionWhenRef_findsIt(self):
        text = """
---
- test1: "{{ tree }}"
  when: (fnord == "FNORD")
"""
        self.sut.add_yaml(text, False)
        expected = set(["tree", "fnord"])
        self.assertSetEqual(self.sut.get_references(), expected)

    def test_simpleDefault_findsIt(self):
        text = """
---
tree: frog 
"""
        self.sut.add_yaml(text, True)
        expected = {"tree": "frog"}
        self.assertDictEqual(self.sut.get_defaults(), expected)

    def test_defaultWithReference_findsIt(self):
        text = """
---
tree: "{{ frog }}"
"""
        self.sut.add_yaml(text, True)
        expected = {"tree": "{{ frog }}"}
        self.assertDictEqual(self.sut.get_defaults(), expected)
        self.assertSetEqual(self.sut.get_references(), set(["frog"]))


if __name__ == '__main__':
    unittest.main()
