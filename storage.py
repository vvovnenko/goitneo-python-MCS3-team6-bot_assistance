import os
import pickle
import constant
from util.data_generator import populateAddressBook, populateNotes


class StorageStrategy:
    def load_from_file(self, container):
        pass

    def save_to_file(self, container):
        with open(self.getFilePath(), "wb+") as fh:
            pickle.dump(container, fh)

    def getFilePath(self):
        dirname = os.path.dirname(__file__)
        return os.path.join(dirname, self.get_storage())

    def get_storage(self):
        pass


class ContactsStorageStrategy(StorageStrategy):

    def load_from_file(self, contacts):
        try:
            with open(self.getFilePath(), "rb") as fh:
                print(f"Loading contacts from file [{self.getFilePath()}]")
                contacts = pickle.load(fh)
            return contacts
        except FileNotFoundError:
            print(f"File not found [{self.getFilePath()}]")
            if len(contacts.data) == 0:
                populateAddressBook(contacts, 100)
            return contacts

    def get_storage(self):
        return constant.FILE_STORAGE_CONTACTS


class NotesStorageStrategy(StorageStrategy):

    def load_from_file(self, notes):
        try:
            with open(self.getFilePath(), "rb") as fh:
                print(f"Loading notes from file [{self.getFilePath()}]")
                notes = pickle.load(fh)
            return notes
        except FileNotFoundError:
            print(f"File not found [{self.getFilePath()}]")
            if len(notes.data) == 0:
                populateNotes(notes, 100)
            return notes

    def get_storage(self):
        return constant.FILE_STORAGE_NOTES


class StorageContext:
    def __init__(self, strategy: StorageStrategy):
        self.strategy = strategy

    def load_from_file(self, container):
        return self.strategy.load_from_file(container)

    def save_to_file(self, container):
        return self.strategy.save_to_file(container)
