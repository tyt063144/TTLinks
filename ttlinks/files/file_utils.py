import hashlib
from abc import ABC, abstractmethod
from typing import Any

from ttlinks.files.file_classifiers import FileClassifier
from ttlinks.files.file_types import FileType


class File(ABC):
    def __init__(self, file_path: str = None, read_method: str = 'r'):
        self._file_path = file_path
        self._read_method = read_method
        self._file_type = None
        self._file_content: Any = None
        self._md5 = None
        self._initialize_file()

    @property
    def file_content(self) -> Any:
        return self._file_content

    @property
    def file_type(self) -> FileType:
        return self._file_type

    @property
    def file_path(self) -> str:
        return self._file_path

    @property
    def md5(self) -> str:
        hash_object = hashlib.md5()
        hash_object.update(self._file_content.encode('utf-8'))
        return hash_object.hexdigest()

    @abstractmethod
    def _validate(self):
        if self._read_method not in ['r', 'w', 'rb', 'wb']:
            raise ValueError(f'Only "r", "w", "rb" and "wb" read method are supported')

    @abstractmethod
    def _read(self):
        pass

    def _initialize_file(self):
        if self._file_path is None:
            self._file_type = FileType.UNKNOWN
            return
        self._validate()
        self._identify_file_type()
        self._read()

    def _identify_file_type(self):
        file_type = FileClassifier.classify_files(self._file_path)
        self._file_type = file_type

    def set_new_path(self, file_path: str) -> None:
        self._file_path = file_path
        self._initialize_file()
