import sys

from PyQt5 import QtWidgets, uic, QtGui, QtCore


class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        uic.loadUi('app.ui', self)

        # Получение экрана и DPI
        screen = QtWidgets.QApplication.screens()[0]
        dpi = screen.logicalDotsPerInch()
        self.scale_factor = dpi / 96  # 96 DPI - обычно стандартный DPI

        # Масштабирование окна с округлением до целых значений
        min_width = int(560 * self.scale_factor)
        min_height = int(500 * self.scale_factor)
        self.setMinimumSize(min_width, min_height)
        self.setMaximumSize(min_width, min_height)

        # Установка иконки для кнопки
        self.buttonBasics.setIcon(QtGui.QIcon('picture.png'))  # Путь к файлу изображения


def main():
    app = QtWidgets.QApplication(sys.argv)

    app.setStyle("fusion")  # Улучшенный стиль для современного вида
    app.setPalette(QtWidgets.QApplication.style().standardPalette())  # Установка стандартной палитры
    window = MyApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
