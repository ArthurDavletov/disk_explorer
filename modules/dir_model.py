"""Файл с модифицированным классом файловой системы для Qt"""
from PySide6.QtCore import Qt, QThread, Signal, QDir
from PySide6.QtWidgets import QFileSystemModel
from pathlib import Path

from modules.logger import Logger


class MyFSModel(QFileSystemModel):
    """Класс модели файловой системы."""
    def __init__(self, parent=None, level: int | str = 40):
        """Инициализатор объекта класса MyFSModel"""
        super().__init__(parent)
        self.__logger = Logger(__name__, level)
        self.counter_cache = {}
        self.active_threads = {}
        for drive in QDir.drives():
            self.fetch_counts(Path(drive.absolutePath()))

    def columnCount(self, parent = ...):
        """Функция переопределяет количество столбцов.
        По умолчанию QFileSystemModel не предоставляет информацию о файлах и директориях"""
        return super().columnCount(parent) + 2

    def data(self, index, role = Qt.DisplayRole):
        """Функция для получения информации в ячейке по определённому индексу."""
        if role == Qt.DisplayRole:
            n = index.column()
            if n == 4:
                path = Path(self.filePath(index))
                return self.counter_cache.get(path, {}).get("files")
            elif n == 5:
                path = Path(self.filePath(index))
                return self.counter_cache.get(path, {}).get("dirs")
        return super().data(index, role)

    def fetch_counts(self, path: Path):
        """Функция для запуска подсчёта количества папок и файлов"""
        if path in self.counter_cache or path in self.active_threads:
            self.__logger.info(f"Данные о папке {path} уже имеются.")
            return
        worker = CounterWorker(path)
        worker.counts_ready.connect(self.update_counts)
        worker.finished.connect(lambda: self.active_threads.pop(path, None))
        self.active_threads[path] = worker
        worker.start()

    def update_counts(self, path: Path, counts):
        """Функция для обновления о количестве."""
        self.counter_cache[path] = counts
        index = self.index(str(path))
        self.dataChanged.emit(index, index)
        self.__logger.info(f"Информация о {path} обновлена.")

    def fetchMore(self, parent):
        """Функция дл обновления информации."""
        super().fetchMore(parent)
        if parent.isValid():
            path = Path(self.filePath(parent))
            self.fetch_counts(path)

    def headerData(self, section, orientation, role = ...):
        """Получения информации о заголовке таблицы"""
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            match section:
                case 0: return "Имя"
                case 1: return "Размер"
                case 2: return "Тип"
                case 3: return "Дата изменения"
                case 4: return "Файлов"
                case 5: return "Папок"
        return super().headerData(section, orientation, role)


def files_dirs_count(path: Path) -> tuple[int | None, int | None]:
    """Функция подсчёта файлов и директорий

    :param path: pathlib.Path-объект, представляющий директорию
    :return: возвращает кортеж из двух элементов: количеств файлов и папок внутри указанной директории."""
    if not path.is_dir():
        return None, None
    files, dirs = 0, 0
    try:
        for child in path.iterdir():
            if child.is_file():
                files += 1
            elif child.is_dir():
                dirs += 1
    except PermissionError:
        return None, None
    return files, dirs


class CounterWorker(QThread):
    """Класс для параллельного подсчёта файлов и папок"""
    counts_ready = Signal(Path, dict)  # Сигнал для передачи результатов

    def __init__(self, path: Path):
        super().__init__()
        self.path: Path = path

    def run(self):
        file_count, folder_count = files_dirs_count(self.path)
        self.counts_ready.emit(self.path, {"files": file_count, "dirs": folder_count})

if __name__ == '__main__':
    pass