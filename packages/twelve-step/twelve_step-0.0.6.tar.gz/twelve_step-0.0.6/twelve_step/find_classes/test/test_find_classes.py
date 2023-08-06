import unittest

from twelve_step.find_classes.find_classes import find_classes

FILE_BASE_PATH = "./twelve_step/find_classes/test/resources"

IMPORTED_CLASSES = ["C", "D"]


class FindClassesTest(unittest.TestCase):
    def test_whenFindingClassesInFile_thenAllClassesAreFound(self):
        classes = find_classes(f"{FILE_BASE_PATH}/classes.py", IMPORTED_CLASSES)

        self.assertEqual(2, len(classes))
        self.assertIn(("A", IMPORTED_CLASSES), classes)
        self.assertIn(("B", IMPORTED_CLASSES), classes)
