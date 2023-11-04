import pickle
from app import constant
from app.util.data_generator import populateAddressBook, populateNotes
from app.contacts import AddressBook
from app.notes import NoteBook
from pathlib import Path


class DataStorage:
    def __init__(self):
        self.storage_path = self.build_file_path()
        self.__book = None
        self.__notes = None

    @property
    def contacts(self) -> AddressBook:
        return self.__book

    @property
    def notes(self) -> NoteBook:
        return self.__notes

    @staticmethod
    def build_file_path():
        root_dir = Path.cwd() / constant.STORAGE_PATH
        if not root_dir.exists():
            root_dir.mkdir()
        storage_file = root_dir / constant.STORAGE_FILE_NAME
        return str(storage_file)

    def __enter__(self) -> None:
        try:
            with open(self.storage_path, "rb") as fh:
                self.__book, self.__notes = pickle.load(fh)
        except FileNotFoundError:
            pass

        if not isinstance(self.__book, AddressBook):
            self.__book = AddressBook()
            populateAddressBook(self.__book, 10)
        if not isinstance(self.__notes, NoteBook):
            self.__notes = NoteBook()
            populateNotes(self.__notes, 50)

    def __exit__(self, exception_type, exception_value, traceback):
        with open(self.storage_path, "wb+") as fh:
            pickle.dump([self.__book, self.__notes], fh)
        self.__book = None
        self.__notes = None


storage = DataStorage()
