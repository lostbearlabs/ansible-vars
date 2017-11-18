import unittest
from ansiblevars.text_analyzer import TextAnalyzer


class TestTextAnalyzer(unittest.TestCase):
    def setUp(self):
        self.sut = TextAnalyzer()

    def test_simpleRef_findsIt(self):
        text = "{{ tree }}"
        self.sut.add_text(text)
        expected = set(["tree"])
        self.assertSetEqual(self.sut.get_references(), expected)

    def test_refWithPipe_findsIt(self):
        text = "{{ tree | lower }}"
        self.sut.add_text(text)
        expected = set(["tree"])
        self.assertSetEqual(self.sut.get_references(), expected)

    def test_refInLoop_findsIt(self):
        text = "{% for x in tree %}"
        self.sut.add_text(text)
        expected = set(["tree"])
        self.assertSetEqual(self.sut.get_references(), expected)

if __name__ == '__main__':
    unittest.main()
