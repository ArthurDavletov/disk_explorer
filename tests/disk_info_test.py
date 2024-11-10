import unittest
import os


class TestDirectory(unittest.TestCase):
    def setUp(self):
        """
        test_dir
        ├── 1
        │   ├── 1
        │   ├── 2
        │   └── 3
        ├── 2
        │   ├── anime.json
        │   ├── jj.ba
        │   └── minecraft.exe
        ├── 3
        ├── file.py
        └── text.txt
        """
        os.makedirs("./test/1/2/3")
        os.mkdir("./test/1/1/")

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
