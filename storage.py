import os
import pickle
import constant
from util.data_generator import populateAddressBook, populateNotes
from contacts import AddressBook
from notes import NoteBook


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
        data_dir = os.path.join(constant.STORAGE_PATH)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        return os.path.join(os.path.dirname(__file__), data_dir, constant.STORAGE_FILE_NAME)

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
