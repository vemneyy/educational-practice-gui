import sys

from PyQt6 import uic, QtWidgets
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtWidgets import QMainWindow


class TheoryWindow(QMainWindow):
    def __init__(self, theory_number):
        super().__init__()
        uic.loadUi('ui/theory_template.ui', self)
        self.main_window = MainWindow()
        self.current_page = 1
        self.total_pages = 3
        self.window_name = 'Теория'
        self.theory_number = theory_number  # Сохраняем номер теории
        self.buttonRevert.setEnabled(False)
        self.buttonBack.clicked.connect(self.openMainWindow)
        self.buttonForward.clicked.connect(self.loadNextPage)
        self.buttonRevert.clicked.connect(self.loadPreviousPage)

        self.buttonPrint.clicked.connect(self.printDocument)  # Connect print button

        self.loadTextFromFile()

    def openMainWindow(self):
        self.main_window.show()
        self.close()

    def loadTextFromFile(self):
        try:
            file_path = f'theory/theory_{self.theory_number}/page_{self.current_page}.html'
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
                self.textBrowser.setHtml(html_content)

            self.buttonRevert.setEnabled(self.current_page > 1)

            if self.current_page < self.total_pages:
                self.buttonForward.setEnabled(True)
                self.buttonRevert.move(950, 100)
            else:
                self.buttonForward.setEnabled(False)
        except FileNotFoundError:
            self.textBrowser.setHtml('<p>Файл не найден.</p>')
        except Exception as e:
            self.textBrowser.setHtml(f'<p>Ошибка при загрузке файла: {e}</p>')

    def loadNextPage(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.loadTextFromFile()
        else:
            self.buttonForward.setVisible(False)

    def loadPreviousPage(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.loadTextFromFile()

    def printDocument(self):
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            self.textBrowser.print(printer)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.theory_window = None
        self.auth_window = None
        uic.loadUi('ui/app.ui', self)

        for i in range(1, 6):
            getattr(self, f'buttonBasics_{i}').clicked.connect(lambda _, x=i: self.open_theory_window(x))

    def open_theory_window(self, theory_number):
        self.theory_window = TheoryWindow(theory_number)
        self.theory_window.show()
        self.close()


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")  # Enhanced style for a modern look

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
