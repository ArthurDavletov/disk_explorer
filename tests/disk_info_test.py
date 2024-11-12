import unittest
import os
from shutil import rmtree
from modules.disk_info import Directory
from modules.exceptions import DirectoryNotFoundError


class TestDirectory(unittest.TestCase):
    def setUp(self):
        """
        test_dir
        ├── 1
        │   ├── 1
        │   ├── 2
        │   └── 3
        ├── 2
        │   ├── anime.json
        │   ├── jj.ba
        │   └── minecraft.exe
        ├── 3
        ├── file.py
        └── text.txt
        """
        os.makedirs("./test_dir/1/1/")
        os.mkdir("./test_dir/1/2/")
        os.mkdir("./test_dir/1/3/")
        os.mkdir("./test_dir/2/")
        with (open("./test_dir/2/anime.json", "w"),
              open("./test_dir/2/jj.ba", "w"),
              open("./test_dir/2/minecraft.exe", "w")):
            pass
        os.mkdir("./test_dir/3/")
        with open("./test_dir/file.py", "w"), open("./test_dir/text.txt", "w"):
            pass
        self.directory = Directory("./test_dir/")
        self.directory.update()

    def test_simple_check(self):
        self.assertEqual(self.directory.n_files, 2)
        self.assertEqual(self.directory.n_dirs, 3)

    def test_not_existing_directory(self):
        with self.assertRaises(DirectoryNotFoundError):
            Directory("abcdef_qwerty_10112024")

    def tearDown(self):
        rmtree("./test_dir/")


if __name__ == "__main__":
    unittest.main()
