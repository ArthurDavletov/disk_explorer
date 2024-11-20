import os
from PySide6.QtWidgets import QApplication, QMainWindow, QHeaderView
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QFile, QTextStream
from pathlib import Path

from modules.dir_model import MyFSModel
from ui.compiled_ui import Ui_MainWindow
import sys


class DiskExplorer(QMainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.night_mode: bool = False
        self.path_history: None | Path = None
        self.__after_init()

    def __after_init(self):
        self.ui.change_color_button.clicked.connect(self.__toggle_night_mode)
        self.ui.back_button.clicked.connect(self.__on_back_button_clicked)
        self.ui.forward_button.clicked.connect(self.__on_forward_button_clicked)
        self.ui.table_view.doubleClicked.connect(self.__on_cell_clicked)

        self.model = MyFSModel()
        self.model.setRootPath(self.model.rootPath())
        self.ui.table_view.setRootIndex(self.model.index(self.model.rootPath()))
        self.ui.table_view.setModel(self.model)

        self.__resize_header()

    def __resize_header(self):
        header = self.ui.table_view.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        for i in range(1, 6):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)

    def __on_cell_clicked(self, index):
        path_str = self.model.filePath(index)
        path = Path(path_str)
        if path.is_dir():
            self.ui.table_view.setRootIndex(self.model.index(path_str))
            self.model.setRootPath(path_str)
            self.path_history = path
            self.__update_counts(path)
            self.__update_path_line()
        else:
            os.startfile(path)

    def __update_counts(self, path: Path):
        for child in path.iterdir():
            self.model.fetch_counts(child)

    def __update_path_line(self):
        self.ui.path_edit.setText(self.model.rootPath())

    def __on_back_button_clicked(self):
        current_index = self.ui.table_view.rootIndex()
        parent_index = self.model.parent(current_index)
        if parent_index.isValid():
            self.ui.table_view.setRootIndex(parent_index)
            path_str = self.model.filePath(parent_index)
            self.model.setRootPath(path_str)
            self.path_history = Path(path_str)
        else:
            self.model.setRootPath("")
            self.ui.table_view.setRootIndex(self.model.index(self.model.rootPath()))
            self.ui.path_edit.clear()
            self.path_history = None
        self.__update_path_line()

    def __on_forward_button_clicked(self):
        base = Path(self.model.rootPath())
        target = self.path_history
        if not target.resolve().is_relative_to(base.resolve()):
            return
        print(base, target)
        base /= target.relative_to(base).parts

        self.ui.table_view.setRootIndex(self.model.index(str(base)))
        path_str = self.model.filePath(self.model.index(str(base)))
        self.model.setRootPath(path_str)
        self.__update_path_line()

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
