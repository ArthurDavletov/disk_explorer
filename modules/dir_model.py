import os
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileSystemModel
from modules.directory import Directory


class MyFSModel(QFileSystemModel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def columnCount(self, parent = ...):
        return super().columnCount(parent) + 2

    def headerData(self, section, orientation, role = ...):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            match section:
                case 0:
                    return "Имя"
                case 1:
                    return "Размер"
                case 2:
                    return "Тип"
                case 3:
                    return "Дата изменения"
                case 4:
                    return "Файлов"
                case 5:
                    return "Папок"
        return super().headerData(section, orientation, role)


if __name__ == '__main__':
    pass