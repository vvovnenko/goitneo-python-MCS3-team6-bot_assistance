import pickle
import constant
from util.contacts_generator import populateAddressBook


def load_contacts_from_file(contacts):
    file_name = constant.FILE_STORAGE
    try:
        with open(file_name, "rb") as fh:
            print(f"Loading contacts from file [{file_name}]")
            contacts = pickle.load(fh)
        return contacts
    except FileNotFoundError:
        print(f"File not found [{file_name}]")
        if len(contacts.data) == 0:
            populateAddressBook(contacts, 100)
        return contacts


def save_contacts_to_file(contacts):
    with open(constant.FILE_STORAGE, "wb+") as fh:
        pickle.dump(contacts, fh)
