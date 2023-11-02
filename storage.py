import pickle
import constant
from util.data_generator import populateAddressBook, populateNotes
from contacts import AddressBook
from notes import NoteBook


class DataStorage:
    def __init__(self):
        self.filename = constant.FILE_STORAGE
        self.__book = None
        self.__notes = None

    @property
    def contacts(self) -> AddressBook:
        return self.__book

    @property
    def notes(self) -> NoteBook:
        return self.__notes

    def __enter__(self) -> None:
        try:
            with open(self.filename, "rb") as fh:
                self.__book, self.__notes = pickle.load(fh)
        except FileNotFoundError:
            pass

        if not isinstance(self.__book, AddressBook):
            self.__book = AddressBook()
            populateAddressBook(self.__book, 100)
        if not isinstance(self.__notes, NoteBook):
            self.__notes = NoteBook()
            populateNotes(self.__notes, 100)

    def __exit__(self, exception_type, exception_value, traceback):
        with open(self.filename, "wb") as fh:
            pickle.dump([self.__book, self.__notes], fh)
        self.__book = None
        self.__notes = None

storage = DataStorage()
