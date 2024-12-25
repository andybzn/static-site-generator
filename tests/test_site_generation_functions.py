import unittest
from src.site_generation_functions import extract_title


class TestTitleExtraction(unittest.TestCase):
    def test_eq(self):
        self.assertEqual("hello there", extract_title("# hello there"))

    def test_no_extra(self):
        self.assertEqual(
            "hello there", extract_title("# hello there\nthis shouldn't be here")
        )

    def test_invalid_title_none(self):
        with self.assertRaises(ValueError):
            extract_title("hello")

    def test_invalid_title_spacing(self):
        with self.assertRaises(ValueError):
            extract_title("#hello")

    def test_invalid_title_level(self):
        with self.assertRaises(ValueError):
            extract_title("## hello")


if "__name__" == "__main__":
    unittest.main()
