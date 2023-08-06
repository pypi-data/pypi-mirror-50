import unittest

from ..find_imports_in_file import find_imports_in_file

FILE_BASE_PATH = "./twelve_step/find_imports/test/resources"


class FindImportsInFileTest(unittest.TestCase):
    def test_whenFindingImports_thenLineStartingWithFromKeyWordAreRetained(self):
        lines = find_imports_in_file(f"{FILE_BASE_PATH}/test_file.py")

        self.assertEqual(2, len(lines))
        self.assertIn(
            "from twelve_step.find_classes.find_classes import find_classes\n", lines
        )
        self.assertIn(
            "from twelve_step.find_imported_classes.find_imported_classes_in_imports import     find_imported_classes_in_imports,",
            lines,
        )

    def test_givenFromIsPresentInNaming_whenFindingImports_thenItIsNotConfusedWithAnActualImports(
        self
    ):
        lines = find_imports_in_file(f"{FILE_BASE_PATH}/file_containing_from.py")

        self.assertEqual(0, len(lines))

    def test_givenMultiLineImport_thenAllImportsAreContractedToALine(self):
        lines = find_imports_in_file(f"{FILE_BASE_PATH}/multi_line_imports.py")

        self.assertIn("from main import     find_imports,     find_classes", lines)
