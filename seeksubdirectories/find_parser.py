from typing import Generator, List, Tuple
from dataclasses import dataclass


@dataclass
class Directory(object):
    def __init__(self, fullpath: str, name: str, directories: List['Directory']):
        self._fullpath = fullpath
        self._name = name
        self._directories = directories
        self._checksum = 0

    @property
    def fullpath(self):
        return self._fullpath

    @property
    def name(self):
        return self._name

    @property
    def directories(self):
        return self._directories

    def add_directory(self, directory: 'Directory'):
        self._checksum = 0
        self._directories.append(directory)

    @property
    def checksum(self):
        self._maybe_recalc_checksum()
        return self._checksum

    def _maybe_recalc_checksum(self):
        if self._checksum == 0:
            dir_checksums = [d.checksum for d in self._directories]
            self._checksum = hash((self._name, tuple(dir_checksums)))
        return self._checksum

    def __repr__(self):
        return f'Directory(fullpath="{self.fullpath}", name="{self.name}", checksum={self.checksum}, directories={self.directories})'


def parse_find_output(lines: List[str], sep: str) -> Directory:
    if not lines or not sep:
        raise ValueError('Must provide lines and separator cannot be None')

    def _split_path(path: str) -> List[str]:
        path_strs = path.strip().split(sep)
        return [s for s in path_strs if s]

    def _parse(depth: int, index: int) -> Tuple[int, Directory]:
        full_path_str = lines[index].strip()
        shallow_path = _split_path(lines[index])[:depth + 1]
        directory_name = shallow_path[-1]
        directories: List[Directory] = []

        def _path_changed() -> bool:
            if index >= len(lines):
                return True
            new_shallow_path = _split_path(lines[index])[:depth + 1]
            if new_shallow_path != shallow_path:
                return True
            return False

        while True:
            if _path_changed():
                return index, Directory(fullpath=full_path_str, name=directory_name, directories=directories)

            deep_path = _split_path(lines[index])
            path_depth = len(deep_path)

            if path_depth > depth + 1:
                index, subdirectory = _parse(depth + 1, index)
                directories.append(subdirectory)
            else:
                index += 1

    _, output = _parse(0, 0)
    return output
