from PySide6.QtWidgets import QApplication, QMainWindow
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
        self.night_mode = not self.night_mode
        styles = {
            self.ui.centralwidget: u"background-color: rgb(19, 19, 19); color: rgb(255,255,255);",
            self.ui.back_button: u"background-color: rgb(74, 74, 74); color: rgb(255,255,255);",
            self.ui.change_color_button: u"background-color: rgb(74, 74, 74); color: rgb(255,255,255);",
            self.ui.forward_button: u"background-color: rgb(74, 74, 74); color: rgb(255,255,255);",
            self.ui.path_edit: u"background-color: rgb(74, 74, 74); color: rgb(255,255,255);",
            self.ui.up_button: u"background-color: rgb(74, 74, 74); color: rgb(255,255,255);",
            self.ui.tableView: u"background-color: rgb(74, 74, 74);"
        }
        if self.night_mode:
            for elem, stylesheet in styles.items():
                elem.setStyleSheet(stylesheet)
        else:
            for elem in styles:
                elem.setStyleSheet(u"")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DiskExplorer()
    window.show()
    sys.exit(app.exec())
