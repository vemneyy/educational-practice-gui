import os
import random
import sys

from PyQt6 import uic, QtWidgets
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtWidgets import QMainWindow, QDialog


class ConfirmationDialog(QDialog):
    def __init__(self, parent=None):
        super(ConfirmationDialog, self).__init__(parent)
        uic.loadUi('ui/window_confirm.ui', self)
        self.buttonYes.clicked.connect(self.accept)
        self.buttonNo.clicked.connect(self.reject)


class ConfirmationDialog_Test(QDialog):
    def __init__(self, parent=None):
        super(ConfirmationDialog_Test, self).__init__(parent)
        uic.loadUi('ui/window_test_confirm.ui', self)
        self.buttonYes.clicked.connect(self.accept)
        self.buttonNo.clicked.connect(self.reject)


class TestWindow(QMainWindow):
    def __init__(self):
        super(TestWindow, self).__init__()
        self.main_window = MainWindow()
        self.test_window = None
        uic.loadUi('ui/test_template.ui', self)

        self.buttonFinal.setEnabled(False)

        self.buttonFinal.clicked.connect(self.showConfirmationDialog_Final)
        self.buttonMain.clicked.connect(self.showConfirmationDialog)
        self.buttonBack.clicked.connect(self.goBack)
        self.buttonForward.clicked.connect(self.goForward)

        self.total_tabs = 9  # Total number of tabs
        self.current_tab_index = 0  # Starting index

        self.updateNavigationButtons()

    def showConfirmationDialog(self):
        dialog = ConfirmationDialog(self)
        if dialog.exec():
            self.openMainWindow()

    def showConfirmationDialog_Final(self):
        dialog = ConfirmationDialog_Test(self)
        if dialog.exec():
            self.openMainWindow()

    def openMainWindow(self):
        self.main_window.show()
        self.close()

    def goBack(self):
        if self.current_tab_index > 0:
            self.current_tab_index -= 1
            self.tabWidget.setCurrentIndex(self.current_tab_index)
            self.updateNavigationButtons()

    def goForward(self):
        if self.current_tab_index < self.total_tabs - 1:
            self.current_tab_index += 1
            self.tabWidget.setCurrentIndex(self.current_tab_index)
            self.updateNavigationButtons()

    def updateNavigationButtons(self):
        self.buttonBack.setEnabled(self.current_tab_index > 0)
        self.buttonForward.setEnabled(self.current_tab_index < self.total_tabs - 1)


class TrainerWindow(QMainWindow):
    def __init__(self):
        super(TrainerWindow, self).__init__()
        self.calculated_r_2 = None
        self.I1 = None
        self.R1 = None
        self.R2 = None
        self.I2 = None
        self.calculated_r = None
        self.main_window = MainWindow()
        self.trainer_window = None
        uic.loadUi('ui/trainer_template.ui', self)

        self.buttonMain.clicked.connect(self.openMainWindow)
        self.buttonMain_2.clicked.connect(self.openMainWindow)
        self.buttonMain_3.clicked.connect(self.openMainWindow)
        self.buttonGenerate.clicked.connect(self.generateValues)  # Связываем кнопку с методом генерации
        self.buttonSubmit_1.clicked.connect(self.submitValue)
        self.buttonGenerate_2.clicked.connect(self.generateValues)  # Связываем кнопку с методом генерации
        self.buttonGenerate_3.clicked.connect(self.generateValues)  # Связываем кнопку с методом генерации

        self.file_paths = {
            'exFirst_1': 'practice/practice_1.html',
            'exFirst_2': 'practice/practice_2.html',
            'exFirst_3': 'practice/practice_3.html'
        }

        self.generateValues()

    def openMainWindow(self):
        self.main_window.show()
        self.close()

    def load_html(self):
        for key, path in self.file_paths.items():
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    html_content = file.read()
                    getattr(self, key).setHtml(html_content)
            except FileNotFoundError:
                getattr(self, key).setHtml('<p>Файл не найден.</p>')
                self.buttonForward.setEnabled(False)
            except Exception as e:
                getattr(self, key).setHtml(f'<p>Ошибка при загрузке файла: {e}</p>')
                self.buttonForward.setEnabled(False)

    def generateValues(self):
        while True:
            self.I1 = random.randint(1, 20)
            self.R1 = random.randint(10, 100)
            self.R2 = random.randint(10, 100)
            self.I2 = random.randint(1, 20)
            self.R1_2 = random.randint(1, 100)
            self.R2_2 = random.randint(1, 100)
            self.R3_2 = random.randint(1, 100)
            self.R4_2 = random.randint(1, 100)

            calculated_r = ((self.I1 - self.I2) * (self.R1 + self.R2)) / self.I2
            calculated_r_2 = self.R1_2 + (self.R2_2 * self.R3_2) / (self.R2_2 + self.R3_2) + self.R4_2

            if calculated_r >= 1 and calculated_r_2 >= 1:
                self.calculated_r = round(calculated_r, 2)
                self.calculated_r_2 = round(calculated_r_2, 2)
                break


        try:
            for key, path in self.file_paths.items():
                with open(path, 'r', encoding='utf-8') as file:
                    html_content = file.read()

                html_content = html_content.replace('{I1}', f'{self.I1}')
                html_content = html_content.replace('{R1}', f'{self.R1}')
                html_content = html_content.replace('{R2}', f'{self.R2}')
                html_content = html_content.replace('{I2}', f'{self.I2}')
                html_content = html_content.replace('{R1_2}', f'{self.R1_2}')
                html_content = html_content.replace('{R2_2}', f'{self.R2_2}')
                html_content = html_content.replace('{R3_2}', f'{self.R3_2}')
                html_content = html_content.replace('{R4_2}', f'{self.R4_2}')

                getattr(self, key).setHtml(html_content)
                self.result_1.setText("")
        except FileNotFoundError:
            getattr(self, key).setHtml('<p>Файл не найден.</p>')
        except Exception as e:
            getattr(self, key).setHtml(f'<p>Ошибка при загрузке файла: {e}</p>')

    def submitValue(self):
        try:
            entered_r = float(self.line_1.text())  # Get the text from line_1 and convert to float
            if entered_r == round(self.calculated_r, 2):
                self.result_1.setText("Результат верный!")
            else:
                self.result_1.setText("Результат неверный, попробуйте снова!")

            print(f"Entered value: {entered_r}")  # Print the entered value
            print(f"Calculated value: {round(self.calculated_r, 2)}")  # Print the calculated value
        except ValueError:
            print("Please enter a valid number in line_1.")
        except ZeroDivisionError:
            print("Division by zero occurred in the calculation.")


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
        self.test_window = None
        self.trainer_window = None
        self.theory_window = None
        uic.loadUi('ui/app.ui', self)

        self.buttonBasics_1.clicked.connect(lambda: self.open_theory_window(1, 'Основы электричества'))
        self.buttonBasics_2.clicked.connect(lambda: self.open_theory_window(2, 'Электрический ток'))
        self.buttonBasics_3.clicked.connect(lambda: self.open_theory_window(3, 'Электрическая мощность'))
        self.buttonBasics_4.clicked.connect(lambda: self.open_theory_window(4, 'Закон Ома'))
        self.buttonBasics_5.clicked.connect(lambda: self.open_theory_window(5, 'Магнетизм'))
        self.buttonPractice_1.clicked.connect(lambda: self.open_test_window())
        self.buttonPractice_2.clicked.connect(lambda: self.open_trainer_window())

    def open_theory_window(self, theory_number, window_name):
        self.theory_window = TheoryWindow(theory_number, window_name)
        self.theory_window.show()
        self.close()

    def open_test_window(self):
        self.test_window = TestWindow()
        self.test_window.show()
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
