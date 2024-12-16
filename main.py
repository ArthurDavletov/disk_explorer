"""Главный файл, запускающий оконное приложение"""
import sys
from PySide6.QtWidgets import QApplication
from modules.disk_explorer import DiskExplorer


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DiskExplorer()
    window.show()
    sys.exit(app.exec())
