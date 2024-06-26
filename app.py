import os
import random
import sys

from PyQt6 import uic, QtWidgets
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtWidgets import QMainWindow, QDialog


# Класс для отображения результатов теста
class TestResult(QMainWindow):
    def __init__(self, results, first_name, last_name):
        super(TestResult, self).__init__()
        uic.loadUi('ui/test_result.ui', self)
        self.buttonMain.clicked.connect(self.open_main_window)
        self.update_labels(results)
        self.label_2.setText(f"Результаты пользователя \"{first_name.capitalize()} {last_name.capitalize()}\"")

    '''
    Открыть главное окно приложения
    '''
    def open_main_window(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

    '''
    Обновить метки с результатами выполнения заданий
    '''
    def update_labels(self, results):
        completed_tasks = sum(results)
        total_tasks = len(results)
        self.label.setText(f"{completed_tasks}/{total_tasks}")
        for i, result in enumerate(results, start=1):
            label = getattr(self, f"exersise_{i}")
            if result:
                label.setText("выполнено")
            else:
                label.setText("не выполнено")


# Класс для окна ввода данных пользователя перед началом теста
class TestSign(QMainWindow):
    def __init__(self):
        super(TestSign, self).__init__()
        uic.loadUi('ui/test_sign.ui', self)
        self.buttonStart.clicked.connect(self.open_test_window)

    '''
    Открыть окно теста с передачей введенных данных пользователя
    '''
    def open_test_window(self):
        self.main_window = TestWindow(self.line_firstName.text(), self.line_lastName.text())
        self.main_window.show()
        self.close()


# Класс диалога подтверждения действий (навигация по окнам)
class ConfirmationDialog(QDialog):
    def __init__(self, parent=None):
        super(ConfirmationDialog, self).__init__(parent)
        uic.loadUi('ui/window_confirm.ui', self)
        self.buttonYes.clicked.connect(self.accept)
        self.buttonNo.clicked.connect(self.reject)


# Класс диалога подтверждения завершения теста
class ConfirmationDialogTest(QDialog):
    def __init__(self, parent=None):
        super(ConfirmationDialogTest, self).__init__(parent)
        uic.loadUi('ui/window_test_confirm.ui', self)
        self.buttonYes.clicked.connect(self.accept)
        self.buttonNo.clicked.connect(self.reject)


# Класс для окна теста
class TestWindow(QMainWindow):
    def __init__(self, first_name, last_name):
        super(TestWindow, self).__init__()
        self.main_window = MainWindow()
        uic.loadUi('ui/test_template.ui', self)
        self.first_name = first_name
        self.last_name = last_name
        self.buttonFinal.setEnabled(False)
        self.buttonFinal.clicked.connect(self.showConfirmationDialog_Final)
        self.buttonMain.clicked.connect(self.showConfirmationDialog)
        self.buttonBack.clicked.connect(self.goBack)
        self.buttonForward.clicked.connect(self.goForward)
        self.total_tabs = 9
        self.current_tab_index = 0
        self.tabWidget.currentChanged.connect(self.updateCurrentTabIndex)
        self.updateNavigationButtons()

    '''
    Показать диалог подтверждения возврата на главное окно
    '''
    def showConfirmationDialog(self):
        dialog = ConfirmationDialog(self)
        if dialog.exec():
            self.openMainWindow()

    '''
    Показать диалог подтверждения завершения теста
    '''
    def showConfirmationDialog_Final(self):
        dialog = ConfirmationDialogTest(self)
        if dialog.exec():
            self.checkFinalAnswers()
            self.openResultWindow()

    '''
    Открыть окно с результатами теста
    '''
    def openResultWindow(self):
        results = self.checkFinalAnswers()
        self.trainer_window = TestResult(results, self.first_name, self.last_name)
        self.trainer_window.show()
        self.close()

    '''
    Открыть главное окно приложения
    '''
    def openMainWindow(self):
        self.main_window.show()
        self.close()

    '''
    Переход на предыдущую вкладку
    '''
    def goBack(self):
        if self.current_tab_index > 0:
            self.current_tab_index -= 1
            self.tabWidget.setCurrentIndex(self.current_tab_index)
            self.updateNavigationButtons()

    '''
    Переход на следующую вкладку
    '''
    def goForward(self):
        if self.current_tab_index < self.total_tabs - 1:
            self.current_tab_index += 1
            self.tabWidget.setCurrentIndex(self.current_tab_index)
            self.updateNavigationButtons()

    '''
    Обновление текущего индекса вкладки
    '''
    def updateCurrentTabIndex(self, index):
        self.current_tab_index = index
        self.updateNavigationButtons()

    '''
    Обновление состояния кнопок навигации
    '''
    def updateNavigationButtons(self):
        self.buttonBack.setEnabled(self.current_tab_index > 0)
        self.buttonForward.setEnabled(self.current_tab_index < self.total_tabs - 1)
        if not self.buttonFinal.isEnabled() and self.current_tab_index == self.total_tabs - 1:
            self.buttonFinal.setEnabled(True)

    '''
    Проверка правильности ответов на финальные вопросы
    '''
    def checkFinalAnswers(self):
        questions = [
            (self.radioButton_2.isChecked, True),
            (self.radioButton_19.isChecked, True),
            (lambda: self.line_2.text().strip().lower() == "поляризация".lower(), True),
            (self.radioButton_6.isChecked, True),
            (lambda: self.line_3.text().strip().lower() == "электромагнитная индукция".lower(), True),
            (self.radioButton_10.isChecked, True),
            (lambda: self.line_4.text().strip().lower() == "сверхпроводимость".lower(), True),
            (self.radioButton_13.isChecked, True),
            (lambda: self.line_5.text().strip().lower() == "постоянный ток".lower(), True)
        ]
        correct_answers = 0
        results = []
        for question, expected in questions:
            if question() == expected:
                correct_answers += 1
                results.append(True)
            else:
                results.append(False)
        return results


# Класс для окна тренажера
class TrainerWindow(QMainWindow):
    def __init__(self):
        super(TrainerWindow, self).__init__()
        self.main_window = MainWindow()
        uic.loadUi('ui/trainer_template.ui', self)
        self.setup_connections()
        self.file_paths = {
            'exFirst_1': 'practice/practice_1.html',
            'exFirst_2': 'practice/practice_2.html',
            'exFirst_3': 'practice/practice_3.html'
        }
        self.generateValues()

    '''
    Настройка сигналов для кнопок
    '''
    def setup_connections(self):
        buttons_to_main = [self.buttonMain, self.buttonMain_2, self.buttonMain_3]
        for button in buttons_to_main:
            button.clicked.connect(self.openMainWindow)
        buttons_to_generate = [self.buttonGenerate, self.buttonGenerate_2, self.buttonGenerate_3]
        for button in buttons_to_generate:
            button.clicked.connect(self.generateValues)
        self.buttonSubmit_1.clicked.connect(lambda: self.submit_value(self.line_1, self.result_1, self.calculated_r))
        self.buttonSubmit_2.clicked.connect(lambda: self.submit_value(self.line_2, self.result_2, self.calculated_r_2))
        self.buttonSubmit_3.clicked.connect(lambda: self.submit_value(self.line_3, self.result_3, self.calculated_r_3))

    '''
    Открыть главное окно приложения
    '''
    def openMainWindow(self):
        self.main_window.show()
        self.close()

    '''
    Загрузка HTML-файлов в виджеты
    '''
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

    '''
    Генерация случайных значений для тренажера
    '''
    def generateValues(self):
        while True:
            self.set_random_values()
            calculated_r = self.calculate_r()
            calculated_r_2 = self.calculate_r_2()
            calculated_r_3 = self.calculate_r_3()
            if self.valid_calculations(calculated_r, calculated_r_2, calculated_r_3):
                self.calculated_r = round(calculated_r, 2)
                self.calculated_r_2 = round(calculated_r_2, 2)
                self.calculated_r_3 = round(calculated_r_3, 2)
                break
        self.update_html_files()

    '''
    Установить случайные значения для переменных
    '''
    def set_random_values(self):
        self.I1 = random.randint(1, 20)
        self.R1 = random.randint(10, 100)
        self.R2 = random.randint(10, 100)
        self.I2 = random.randint(1, 20)
        self.R1_2 = random.randint(1, 100)
        self.R2_2 = random.randint(1, 100)
        self.R3_2 = random.randint(1, 100)
        self.R4_2 = random.randint(1, 100)
        self.E1 = random.randint(1, 20)
        self.E2 = random.randint(1, 10)
        self.E3 = random.randint(1, 10)
        self.E4 = random.randint(1, 10)

    '''
    Расчет значения сопротивления для первой задачи
    '''
    def calculate_r(self):
        return ((self.I1 - self.I2) * (self.R1 + self.R2)) / self.I2

    '''
    Расчет значения сопротивления для второй задачи
    '''
    def calculate_r_2(self):
        return self.R1_2 + (self.R2_2 * self.R3_2) / (self.R2_2 + self.R3_2) + self.R4_2

    '''
    Расчет значения сопротивления для третьей задачи
    '''
    def calculate_r_3(self):
        return (self.E2 * (1 / self.E3) / (1 / self.E4) ** 2) * self.E1

    '''
    Проверка корректности рассчитанных значений
    '''
    def valid_calculations(self, calculated_r, calculated_r_2, calculated_r_3):
        return calculated_r >= 1 and calculated_r_2 and calculated_r_3 >= 1

    '''
    Обновление HTML-файлов с новыми значениями
    '''
    def update_html_files(self):
        try:
            for key, path in self.file_paths.items():
                with open(path, 'r', encoding='utf-8') as file:
                    html_content = file.read()
                variables = {
                    '{I1}': self.I1, '{R1}': self.R1, '{R2}': self.R2, '{I2}': self.I2,
                    '{R1_2}': self.R1_2, '{R2_2}': self.R2_2, '{R3_2}': self.R3_2, '{R4_2}': self.R4_2,
                    '{E1}': self.E1, '{E2}': self.E2, '{E3}': self.E3, '{E4}': self.E4
                }
                for placeholder, value in variables.items():
                    html_content = html_content.replace(placeholder, str(value))
                getattr(self, key).setHtml(html_content)
                self.result_1.setText("")
                self.result_2.setText("")
                self.result_3.setText("")
        except FileNotFoundError:
            getattr(self, key).setHtml('<p>Файл не найден.</p>')
        except Exception as e:
            getattr(self, key).setHtml(f'<p>Ошибка при загрузке файла: {e}</p>')

    '''
    Отправка значения и проверка корректности ответа
    '''
    def submit_value(self, line_edit, result_label, calculated_value):
        try:
            entered_r = float(line_edit.text())
            if entered_r == calculated_value:
                result_label.setText("Результат верный!")
            else:
                result_label.setText("Результат неверный, попробуйте снова!")
                print(calculated_value)
        except ValueError:
            result_label.setText("Введите корректное значение!")
        except ZeroDivisionError:
            result_label.setText("Ошибка деления на ноль.")


# Класс для окна с теорией
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

    '''
    Получить количество страниц теоретического материала
    '''
    def get_total_pages(self):
        theory_path = f'theory/theory_{self.theory_number}'
        if os.path.exists(theory_path):
            files = os.listdir(theory_path)
            page_files = [f for f in files if f.startswith('page_') and f.endswith('.html')]
            total_pages = len(page_files)
            return total_pages
        return 0

    '''
    Открыть главное окно приложения
    '''
    def openMainWindow(self):
        self.main_window.show()
        self.close()

    '''
    Загрузить текст теоретического материала из файла
    '''
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

    '''
    Загрузка следующей или предыдущей страницы теоретического материала
    '''
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

    '''
    Обновить метку с номером текущей страницы
    '''
    def updatePageLabel(self):
        self.labelPage.setText(f"{self.current_page}/{self.total_pages}")

    '''
    Печать текущей страницы теоретического материала
    '''
    def printDocument(self):
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            self.textBrowser.print(printer)


# Класс для главного окна приложения
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('ui/app.ui', self)
        self.buttonBasics_1.clicked.connect(lambda: self.open_theory_window(1, 'Основы электричества'))
        self.buttonBasics_2.clicked.connect(lambda: self.open_theory_window(2, 'Электрический ток'))
        self.buttonBasics_3.clicked.connect(lambda: self.open_theory_window(3, 'Электрическая мощность'))
        self.buttonBasics_4.clicked.connect(lambda: self.open_theory_window(4, 'Закон Ома'))
        self.buttonBasics_5.clicked.connect(lambda: self.open_theory_window(5, 'Магнетизм'))
        self.buttonPractice_1.clicked.connect(lambda: self.open_test_window())
        self.buttonPractice_2.clicked.connect(lambda: self.open_trainer_window())

    '''
    Открыть окно с теоретическим материалом
    '''
    def open_theory_window(self, theory_number, window_name):
        self.theory_window = TheoryWindow(theory_number, window_name)
        self.theory_window.show()
        self.close()

    '''
    Открыть окно теста
    '''
    def open_test_window(self):
        self.test_window = TestSign()
        self.test_window.show()
        self.close()

    '''
    Открыть окно тренажера
    '''
    def open_trainer_window(self):
        self.trainer_window = TrainerWindow()
        self.trainer_window.show()
        self.close()


# Класс для начального окна приветствия
class HelloWindow(QMainWindow):
    def __init__(self):
        super(HelloWindow, self).__init__()
        uic.loadUi('ui/hello_window.ui', self)
        self.pushButton.clicked.connect(lambda: self.open_main_window())

    '''
    Открыть главное окно приложения
    '''
    def open_main_window(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()


# Основная функция запуска приложения
def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    window = HelloWindow()
    window.show()
    sys.exit(app.exec())


# Запуск приложения
if __name__ == '__main__':
    main()
