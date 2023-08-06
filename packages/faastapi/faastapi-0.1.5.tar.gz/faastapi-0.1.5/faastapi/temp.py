import tempfile
import os
from shutil import copytree, copy2, rmtree
from typing import Optional, List


class TempDirectory:
    def __init__(self, prefix: str = "faastapi_"):
        self.prefix = prefix
        self._path = None
        self.create()

    @property
    def path(self) -> str:
        """
        Return path of temp directory
        """
        if self._path is None:
            raise ValueError("This directory does not exist")
        else:
            return self._path

    def create(self) -> None:
        """
        Create the temp directory. It also sets the path
        """
        self._path = tempfile.mkdtemp(prefix=self.prefix)

    def get_abs_path(self, file_path: str) -> str:
        """
        Get absolute path of given file_path relative to temp directory
        """
        return os.path.join(self.path, file_path)

    def mkdir(self, path: str) -> str:
        """
        Create a directory in temp directory
        """
        dir_path = self.get_abs_path(path)
        return os.makedirs(dir_path, exist_ok=True)

    def touch(self, path: str) -> str:
        """
        Touch a file in temp directory
        """
        file_path = self.get_abs_path(path)
        with open(file_path, "a+") as _file:
            _file.write("")
        return file_path

    def write(self, content: str, path: str) -> str:
        """
        Write a file in temporary dict (path must be relative to directory path)
        """
        output_path = self.get_abs_path(path)
        with open(output_path, "w+") as _file:
            _file.write(content)
        return output_path

    def rm(self, path: str) -> None:
        """
        Remove a single file in directory
        """
        target_path = os.path.join(self.path, path)
        os.remove(target_path)

    def rmtree(self, path: str) -> None:
        """
        Remove given directories recursively
        """
        if len(path) == 0:
            raise ValueError(
                "You must use close method in order to remove the directory"
            )
        target_path = self.get_abs_path(path)
        rmtree(target_path)

    def ls(self, path: Optional[str] = None) -> List[str]:
        """
        List content of temp directory
        """
        if path:
            abs_path = self.get_abs_path(path)
            return os.listdir(abs_path)
        else:
            return os.listdir(self.path)

    def close(self) -> None:
        """
        Close temp directory
        """
        rmtree(self.path)
        self._path = None

    def copy_file(self, src: str, dest: str) -> str:
        """
        Copy a given file from temp directory to given destination
        """
        src_path = self.get_abs_path(src)
        return copy2(src_path, dest)

    def copy(self, dest: str) -> str:
        """
        Copy the whole temp directory to given destination
        """
        return copytree(self.path, dest)
