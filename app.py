import sys

from PyQt6 import QtWidgets, uic


class TheoryWindowSecond(QtWidgets.QMainWindow):
    def __init__(self):
        super(TheoryWindowSecond, self).__init__()
        self.back_window = None
        self.main_window = None
        uic.loadUi('ui/theory_template_other.ui', self)

        self.buttonBack.clicked.connect(self.openBackWindow)
        self.buttonForward.clicked.connect(self.openMainWindow)

    def openMainWindow(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

    def openBackWindow(self):
        self.back_window = TheoryWindow()
        self.back_window.show()
        self.close()


class TheoryWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/theory_template_main.ui', self)
        self.main_window, self.next_window = MainWindow(), TheoryWindowSecond()

        self.buttonBack.clicked.connect(self.openMainWindow)
        self.buttonForward.clicked.connect(self.openNextWindow)

    def openMainWindow(self):
        self.main_window.show()
        self.close()

    def openNextWindow(self):
        self.next_window.show()
        self.close()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.auth_window = None
        uic.loadUi('ui/app.ui', self)

        for i in range(1, 8):
            getattr(self, f'buttonBasics_{i}').clicked.connect(self.open_theory_window)

    def open_theory_window(self):
        self.theory_window = TheoryWindow()
        self.theory_window.show()
        self.close()


def main():
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
