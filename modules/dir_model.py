from PySide6.QtCore import Qt, QThread, Signal, QDir
from PySide6.QtWidgets import QFileSystemModel
from pathlib import Path


class MyFSModel(QFileSystemModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.counter_cache = {}
        self.active_threads = {}
        for drive in QDir.drives():
            self.fetch_counts(Path(drive.absolutePath()))

    def columnCount(self, parent = ...):
        return super().columnCount(parent) + 2

    def data(self, index, role = Qt.DisplayRole):
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
        if path in self.counter_cache or path in self.active_threads:
            return
        worker = CounterWorker(path)
        worker.counts_ready.connect(self.update_counts)
        worker.finished.connect(lambda: self.active_threads.pop(path, None))
        self.active_threads[path] = worker
        worker.start()

    def update_counts(self, path: Path, counts):
        self.counter_cache[path] = counts
        index = self.index(str(path))
        self.dataChanged.emit(index, index)

    def fetchMore(self, parent):
        super().fetchMore(parent)
        if parent.isValid():
            path = Path(self.filePath(parent))
            self.fetch_counts(path)

    def headerData(self, section, orientation, role = ...):
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
    counts_ready = Signal(Path, dict)  # Сигнал для передачи результатов

    def __init__(self, path: Path):
        super().__init__()
        self.path: Path = path

    def run(self):
        file_count, folder_count = files_dirs_count(self.path)
        self.counts_ready.emit(self.path, {"files": file_count, "dirs": folder_count})

if __name__ == '__main__':
    pass