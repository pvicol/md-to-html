import unittest

from utils import extract_title


class TestUtils(unittest.TestCase):
    def test_extract_title(self):
        text = '# Hello'
        expected = 'Hello'
        actual = extract_title(text)

        self.assertEqual(expected, actual)

    def test_extract_title_raises(self):
        text = '''#This is the main title

for the page'''
        with self.assertRaises(ValueError) as cm:
            extract_title(text)

        self.assertEqual(str(cm.exception), 'Could not find a valid title in the markdown')


if __name__ == '__main__':
    unittest.main()
