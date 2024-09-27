from abc import ABC, abstractmethod
from typing import Any

from ttlinks.files.file_classifiers import FileClassifier
from ttlinks.files.file_types import FileType


class File(ABC):
    """
    An abstract base class representing a generic file. This class provides a structured way to interact with
    files by identifying their types and handling their content based on specified methods.

    Attributes:
        _file_path (str): Path to the file.
        _read_method (str): Mode in which the file is opened, e.g., 'r' for read and 'rb' for read binary.
        _file_type (FileType): Enum type representing the type of file, e.g., TEXT, IMAGE, etc.
        _file_content (Any): Content of the file, the type of which may vary depending on the file type.

    Methods:
        file_content: Property to get the content of the file.
        file_type: Property to get the type of the file.
        _validate: Validates the read method.
        _initialize_file: Initializes the file operations including type identification and content reading.
        _identify_file_type: Identifies the file type using a classifier.
        set_new_path: Sets a new file path and re-initializes file operations.
        _read: Abstract method to read the file content; implementation required in subclasses.
    """

    def __init__(self, file_path: str = None, read_method: str = 'r'):
        """
        Initializes the File object with a file path and a method indicating how to read the file.

        Parameters:
            file_path (str): The path to the file.
            read_method (str): The method of reading the file (e.g., 'r', 'rb').
        """
        self._file_path = file_path
        self._read_method = read_method
        self._file_type = None
        self._file_content: Any = None
        self._initialize_file()

    @property
    def file_content(self) -> Any:
        """
        Returns the content of the file.

        Returns:
            Any: The content of the file.
        """
        return self._file_content

    @property
    def file_type(self) -> FileType:
        """
        Returns the type of the file as identified by the FileClassifier.

        Returns:
            FileType: The type of the file.
        """
        return self._file_type

    @abstractmethod
    def _validate(self):
        """
        Validates the read method to ensure it's one of the supported types ('r', 'w', 'rb', 'wb').
        Raises a ValueError if the method is not supported.
        """
        if self._read_method not in ['r', 'w', 'rb', 'wb']:
            raise ValueError(f'Only "r", "w", "rb" and "wb" read method are supported')

    @abstractmethod
    def _read(self):
        """
        Abstract method to read the content of the file. This method needs to be implemented in subclasses to handle
        specific file reading operations based on the file type.
        """
        pass

    def _initialize_file(self):
        """
        Initializes file operations by setting the file type and reading the content if a path is provided.
        """
        if self._file_path is None:
            self._file_type = FileType.UNKNOWN
            return
        self._validate()
        self._identify_file_type()
        self._read()

    def _identify_file_type(self):
        """
        Identifies the file type by passing the file path to the FileClassifier.
        """
        file_type = FileClassifier.classify_files(self._file_path)
        self._file_type = file_type

    def set_new_path(self, file_path: str) -> None:
        """
        Sets a new file path for the file, reinitializing file type and content.

        Parameters:
            file_path (str): The new path for the file.
        """
        self._file_path = file_path
        self._initialize_file()
