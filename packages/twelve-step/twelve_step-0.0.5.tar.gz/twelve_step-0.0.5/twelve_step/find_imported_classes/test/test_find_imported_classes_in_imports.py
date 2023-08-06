import unittest

from ..find_imported_classes_in_imports import find_imported_classes_in_imports

A_CLASS = "A"
ANOTHER_CLASS = "B"
SINGLE_IMPORT = f"from package import {A_CLASS}"
DOUBLE_IMPORT = f"from package import {A_CLASS}, {ANOTHER_CLASS}"
TRAILING_COMMA = f"from package import {A_CLASS},"

A_FILE = "a"


class FindImportedClassesTest(unittest.TestCase):
    def test_whenFindingImportedClasses_thenImportedClassesAreFound(self):
        imported_classes = find_imported_classes_in_imports(A_FILE, [SINGLE_IMPORT])

        self.assertEqual(A_CLASS, imported_classes[1][0])

    def test_givenMultipleImportsInLine_whenFindingImportedClasses_thenAllImportsAreFound(
        self
    ):
        imported_classes = find_imported_classes_in_imports(A_FILE, [DOUBLE_IMPORT])

        self.assertEqual([A_CLASS, ANOTHER_CLASS], imported_classes[1])

    def test_givenMultipleLine_whenFindingImportedClasses_thenAllImportsAreFound(self):
        imported_classes = find_imported_classes_in_imports(
            A_FILE, [SINGLE_IMPORT, DOUBLE_IMPORT]
        )

        self.assertEqual([A_CLASS, A_CLASS, ANOTHER_CLASS], imported_classes[1])

    def test_givenNoImports_whenFindingImportedClasses_thenNoImportsAreFound(self):
        imported_classes = find_imported_classes_in_imports(A_FILE, [])

        self.assertEqual([], imported_classes[1])

    def test_givenTrailing_comma_whenFindingImportedClasses_thenNoEmptyClassImported(
        self
    ):
        imported_classes = find_imported_classes_in_imports(A_FILE, [TRAILING_COMMA])

        self.assertEqual([A_CLASS], imported_classes[1])

    def test_whenFindingImportedClasses_thenFileIsReturnedWithImportedClasses(self):
        imported_classes = find_imported_classes_in_imports(A_FILE, [SINGLE_IMPORT])

        self.assertEqual(A_FILE, imported_classes[0])
