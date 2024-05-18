import os
import random
import sys

from PyQt6 import uic, QtWidgets
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtWidgets import QMainWindow


class TrainerWindow(QMainWindow):
    def __init__(self):
        super(TrainerWindow, self).__init__()
        self.main_window = MainWindow()
        self.trainer_window = None
        uic.loadUi('ui/trainer_template.ui', self)

        self.buttonMain.clicked.connect(self.openMainWindow)
        self.buttonGenerate.clicked.connect(self.generateValues)  # Связываем кнопку с методом генерации

        self.file_path = 'practice/practice_1.html'
        self.generateValues()

    def openMainWindow(self):
        self.main_window.show()
        self.close()

    def load_html(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
                self.exFirst.setHtml(html_content)
        except FileNotFoundError:
            self.exFirst.setHtml('<p>Файл не найден.</p>')
            self.buttonForward.setEnabled(False)
        except Exception as e:
            self.exFirst.setHtml(f'<p>Ошибка при загрузке файла: {e}</p>')
            self.buttonForward.setEnabled(False)

    def generateValues(self):
        I1 = random.randint(1, 10)
        R1 = random.randint(1, 100)
        R2 = random.randint(1, 100)
        I2 = random.randint(1, 10)

        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()

            html_content = html_content.replace('{I1}', f'{I1}')
            html_content = html_content.replace('{R1}', f'{R1}')
            html_content = html_content.replace('{R2}', f'{R2}')
            html_content = html_content.replace('{I2}', f'{I2}')

            self.exFirst.setHtml(html_content)
        except FileNotFoundError:
            self.exFirst.setHtml('<p>Файл не найден.</p>')
        except Exception as e:
            self.exFirst.setHtml(f'<p>Ошибка при загрузке файла: {e}</p>')


class TheoryWindow(QMainWindow):
    def __init__(self, theory_number, window_name):
        super().__init__()
        uic.loadUi('ui/theory_template.ui', self)
        self.main_window = MainWindow()
        self.setWindowTitle(window_name)

        self.current_page = 1
        self.theory_number = theory_number
        self.total_pages = self.get_total_pages()
        self.labelPage.setText(f"{self.current_page}/{self.total_pages}")
        self.buttonQuiz.setVisible(False)
        self.buttonMain.clicked.connect(self.openMainWindow)
        self.buttonForward.clicked.connect(lambda: self.loadPage('next'))
        self.buttonBack.clicked.connect(lambda: self.loadPage('previous'))
        self.buttonPrint.clicked.connect(self.printDocument)

        self.loadTextFromFile()

    def get_total_pages(self):
        theory_path = f'theory/theory_{self.theory_number}'
        if os.path.exists(theory_path):
            files = os.listdir(theory_path)
            page_files = [f for f in files if f.startswith('page_') and f.endswith('.html')]
            total_pages = len(page_files)
            return total_pages
        return 0

    def openMainWindow(self):
        self.main_window.show()
        self.close()

    def loadTextFromFile(self):
        file_path = f'theory/theory_{self.theory_number}/page_{self.current_page}.html'
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
                self.textBrowser.setHtml(html_content)

            self.buttonBack.setEnabled(self.current_page > 1)
            self.buttonForward.setEnabled(self.current_page < self.total_pages)
        except FileNotFoundError:
            self.textBrowser.setHtml('<p>Файл не найден.</p>')
            self.buttonForward.setEnabled(False)
        except Exception as e:
            self.textBrowser.setHtml(f'<p>Ошибка при загрузке файла: {e}</p>')
            self.buttonForward.setEnabled(False)

    def loadPage(self, direction):
        if direction == 'next' and self.current_page < self.total_pages:
            self.current_page += 1
        elif direction == 'previous' and self.current_page > 1:
            self.current_page -= 1

        self.loadTextFromFile()

        if self.current_page == self.total_pages:
            self.buttonForward.setEnabled(False)
            self.buttonQuiz.setVisible(True)
            # self.update_user_cache()

        else:
            self.buttonForward.setEnabled(True)

        if self.current_page == 1:
            self.buttonBack.setEnabled(False)
        else:
            self.buttonBack.setEnabled(True)

        self.updatePageLabel()

    def updatePageLabel(self):
        self.labelPage.setText(f"{self.current_page}/{self.total_pages}")

    def printDocument(self):
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            self.textBrowser.print(printer)

    # def update_user_cache(self):
    #     cache_file = 'user.cache'
    #     cache_data = {}
    #
    #     if os.path.exists(cache_file):
    #         try:
    #             with open(cache_file, 'r', encoding='utf-8') as file:
    #                 cache_data = json.load(file)
    #         except json.JSONDecodeError:
    #             cache_data = {}
    #     else:
    #         with open(cache_file, 'w', encoding='utf-8') as file:
    #             json.dump({}, file)
    #
    #     cache_data[f'theory_{self.theory_number}'] = True
    #
    #     with open(cache_file, 'w', encoding='utf-8') as file:
    #         json.dump(cache_data, file, ensure_ascii=False, indent=4)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.trainer_window = None
        self.theory_window = None
        uic.loadUi('ui/app.ui', self)

        self.buttonBasics_1.clicked.connect(lambda: self.open_theory_window(1, 'Основы электричества'))
        self.buttonBasics_2.clicked.connect(lambda: self.open_theory_window(2, 'Basics'))
        self.buttonBasics_3.clicked.connect(lambda: self.open_theory_window(3, 'Basics'))
        self.buttonBasics_4.clicked.connect(lambda: self.open_theory_window(4, 'Basics'))
        self.buttonBasics_5.clicked.connect(lambda: self.open_theory_window(5, 'Магнетизм'))
        self.buttonPractice_2.clicked.connect(lambda: self.open_trainer_window())

    def open_theory_window(self, theory_number, window_name):
        self.theory_window = TheoryWindow(theory_number, window_name)
        self.theory_window.show()
        self.close()

    def open_trainer_window(self):
        self.trainer_window = TrainerWindow()
        self.trainer_window.show()
        self.close()


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
