import os

class Directory:
    __slots__ = ("__abspath", "__mtime", "__ndirs", "__nfiles")

    def __init__(self, path: os.PathLike | str):
        self.__abspath: str = os.path.abspath(path)
        self.__mtime: float | None = None
        self.__ndirs: int = 0
        self.__nfiles: int = 0
        self.__update()

    def __update(self) -> None:
        mtime = os.path.getmtime(self.abspath)
        if mtime is not None and mtime == self.mtime:
            return
        self.__mtime = mtime
        self.__ndirs, self.__nfiles = 0, 0
        for entry in os.scandir(self.abspath):
            if entry.is_file():
                self.__nfiles += 1
            if entry.is_dir():
                self.__ndirs += 1

    @property
    def abspath(self) -> str:
        return self.__abspath

    @property
    def mtime(self):
        return self.__mtime

    @property
    def ndirs(self):
        return self.__ndirs

    @property
    def nfiles(self):
        return self.__nfiles


if __name__ == '__main__':
    pass
