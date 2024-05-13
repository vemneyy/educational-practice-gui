import sys

from PyQt6 import QtWidgets, uic, QtGui


class AuthWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(AuthWindow, self).__init__()
        self.main_window = None
        uic.loadUi('ui/theory.ui', self)

    def openMainWindow(self):
        self.main_window = MyApp()  # Create an instance of the main window
        self.main_window.show()  # Show the main window
        self.close()  # Close the current (auth) window


class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.auth_window = None
        uic.loadUi('ui/app.ui', self)

        # Set the icon for the button
        self.buttonBasics.setIcon(QtGui.QIcon('ui/buttonBasics.png'))

        # Connect the button click to the function that opens the auth window
        self.buttonBasics.clicked.connect(self.openAuthWindow)

    def openAuthWindow(self):
        self.auth_window = AuthWindow()  # Create an instance of the AuthWindow
        self.auth_window.show()  # Show the auth window
        self.close()  # Close the main window


def main():
    app = QtWidgets.QApplication(sys.argv)

    # Setting the style and palette
    app.setStyle("Fusion")  # Enhanced style for a modern look
    app.setPalette(QtWidgets.QApplication.style().standardPalette())  # Set the standard palette

    window = MyApp()
    window.show()
    sys.exit(app.exec())  # Changed from exec_() to exec()


if __name__ == '__main__':
    main()
