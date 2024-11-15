import os
from PySide6.QtWidgets import QApplication, QMainWindow, QHeaderView
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QFile, QTextStream, Qt
from pathlib import Path

from modules.dir_model import MyFSModel
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
        self.ui.change_color_button.clicked.connect(self.__toggle_night_mode)
        self.ui.back_button.clicked.connect(self.__on_back_button_clicked)
        self.model = MyFSModel()
        self.model.setRootPath(self.model.rootPath())
        self.ui.table_view.setRootIndex(self.model.index(self.model.rootPath()))
        self.ui.table_view.setModel(self.model)
        self.ui.table_view.doubleClicked.connect(self.__on_cell_clicked)
        header = self.ui.table_view.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)

    def __on_cell_clicked(self, index):
        path = self.model.filePath(index)
        if Path(path).is_dir():
            self.ui.table_view.setRootIndex(self.model.index(path))
            self.model.setRootPath(path)
        else:
            os.startfile(path)
        self.__update_counts(path)

    def __update_counts(self, path):
        for child in Path(path).iterdir():
            self.model.fetch_counts(str(child))

    def __on_back_button_clicked(self):
        current_index = self.ui.table_view.rootIndex()
        parent_index = self.model.parent(current_index)
        if parent_index.isValid():
            self.ui.table_view.setRootIndex(parent_index)
        else:
            self.model.setRootPath("")
            self.ui.table_view.setRootIndex(self.model.index(self.model.rootPath()))

    def __toggle_night_mode(self):
        # элемент: [светлый, тёмный]
        icons = {
            self.ui.back_button: [":/icons/arrow_back", ":/icons/arrow_back_white"],
            self.ui.forward_button: [":/icons/arrow_forward", ":/icons/arrow_forward_white"],
            self.ui.refresh_button: [":/icons/refresh", ":/icons/refresh_white"],
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
            self.setStyleSheet(QTextStream(file).readAll())
            file.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DiskExplorer()
    window.show()
    sys.exit(app.exec())
