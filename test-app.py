import unittest
from unittest.mock import patch, mock_open

from PyQt6.QtWidgets import QApplication

from app import TheoryWindow


class TestTheoryWindow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])  # Создаем экземпляр QApplication для тестов

    def setUp(self):
        self.theory_number = 1
        self.window_name = 'Test Window'
        self.theory_window = TheoryWindow(self.theory_number, self.window_name)

    @patch('os.path.exists')
    @patch('os.listdir')
    def test_get_total_pages(self, mock_listdir, mock_exists):
        mock_exists.return_value = True
        mock_listdir.return_value = ['page_1.html', 'page_2.html', 'not_a_page.txt']

        total_pages = self.theory_window.get_total_pages()
        self.assertEqual(total_pages, 2)

    @patch('builtins.open', new_callable=mock_open, read_data='<p>Test Content</p>')
    def test_loadTextFromFile(self, mock_file):
        self.theory_window.current_page = 1
        self.theory_window.loadTextFromFile()

        self.assertEqual(self.theory_window.textBrowser.toHtml(),
                         '<html><head></head><body><p>Test Content</p></body></html>')

    @patch('builtins.open', new_callable=mock_open)
    def test_loadTextFromFile_file_not_found(self, mock_file):
        mock_file.side_effect = FileNotFoundError

        self.theory_window.current_page = 1
        self.theory_window.loadTextFromFile()

        self.assertIn('<p style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">Файл не найден.</p>', self.theory_window.textBrowser.toHtml())

    def test_loadPage(self):
        self.theory_window.total_pages = 3

        self.theory_window.current_page = 1
        self.theory_window.loadPage('next')
        self.assertEqual(self.theory_window.current_page, 2)

        self.theory_window.loadPage('previous')
        self.assertEqual(self.theory_window.current_page, 1)

        self.theory_window.current_page = 3
        self.theory_window.loadPage('previous')
        self.assertEqual(self.theory_window.current_page, 2)




if __name__ == '__main__':
    unittest.main()
