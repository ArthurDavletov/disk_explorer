import os

from modules.exceptions import DirectoryNotFoundError


class Directory:
    __slots__ = ("__abspath", "__m_time", "__n_dirs", "__n_files")

    def __init__(self, path: os.PathLike | str):
        self.__abspath: str = os.path.abspath(path)
        if not os.path.exists(self.abspath):
            raise DirectoryNotFoundError(f"Не удается найти указанную директорию: {self.abspath}")
        self.__m_time: float | None = None
        self.__n_dirs: int | None = None
        self.__n_files: int | None = None

    def update(self) -> None:
        time = os.path.getmtime(self.abspath)
        self.__m_time = time
        self.__n_dirs, self.__n_files = 0, 0
        for entry in os.scandir(self.abspath):
            if entry.is_file():
                self.__n_files += 1
            if entry.is_dir():
                self.__n_dirs += 1

    @property
    def abspath(self) -> str:
        return self.__abspath

    @property
    def m_time(self):
        return self.__m_time

    @property
    def n_dirs(self):
        return self.__n_dirs

    @property
    def n_files(self):
        return self.__n_files


if __name__ == '__main__':
    pass
