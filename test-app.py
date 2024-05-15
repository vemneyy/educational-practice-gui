import unittest

from PyQt6.QtWidgets import QApplication

from app import TheoryWindow

app = QApplication([])


class TestTheoryWindow(unittest.TestCase):
    def setUp(self):
        """Создаём экземпляр TheoryWindow перед каждым тестом."""
        self.theory = TheoryWindow()

    def test_initial_state(self):
        """Тестируем начальное состояние окна теории."""
        self.assertEqual(self.theory.current_page, 1)
        self.assertEqual(self.theory.total_pages, 3)
        self.assertEqual(self.theory.window_name, 'Теория')
        self.assertFalse(self.theory.buttonRevert.isVisible())

    def test_load_next_page(self):
        """Тестируем загрузку следующей страницы."""
        self.theory.loadNextPage()
        self.assertEqual(self.theory.current_page, 2)

    def test_load_text_from_file(self):
        """Тестируем загрузку текста из файла."""
        self.theory.loadTextFromFile()
        # Здесь вам нужно будет адаптировать тест под ожидаемый контент файла
        self.assertNotEqual(self.theory.textBrowser.toHtml(), '')


if __name__ == '__main__':
    unittest.main()
