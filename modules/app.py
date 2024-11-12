from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QFile, QTextStream
from ui.compiled_ui import Ui_MainWindow
import sys


class DiskExplorer(QMainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.night_mode = False
        self.__after_init()

    def __after_init(self):
        self.ui.change_color_button.clicked.connect(self.toggle_night_mode)

    def toggle_night_mode(self):
        # элемент: [светлый, тёмный]
        icons = {
            self.ui.back_button: [":/icons/arrow_back", ":/icons/arrow_back_white"],
            self.ui.forward_button: [":/icons/arrow_forward", ":/icons/arrow_forward_white"],
            self.ui.up_button: [":/icons/arrow_upward", ":/icons/arrow_upward_white"],
            self.ui.change_color_button: [":/icons/light_mode_icon", ":/icons/dark_mode_icon"]
        }
        self.night_mode = not self.night_mode
        if not self.night_mode:
            file = QFile(":/qss/light_mode_qss")
            for elem, path in icons.items():
                elem.setIcon(QPixmap(path[0]))
        else:
            file = QFile(":/qss/night_mode_qss")
            for elem, path in icons.items():
                elem.setIcon(QPixmap(path[1]))
        if file.open(QFile.ReadOnly | QFile.Text):
            app.setStyleSheet(QTextStream(file).readAll())
            file.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DiskExplorer()
    window.show()
    sys.exit(app.exec())
