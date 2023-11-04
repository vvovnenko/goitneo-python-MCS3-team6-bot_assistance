from notes import Note, NoteBook
import constant
from faker import Faker
from contacts import Record, AddressBook
import random


def populateAddressBook(book: AddressBook, quantity):
    print("Populating random contact data")
    fake = Faker()

    for _ in range(quantity):
        record = Record(fake.first_name())
        record.add_phone(str(fake.random_number(digits=10, fix_len=True)))
        if random.randint(0, 1):
            record.add_birthday(fake.date_of_birth(
                minimum_age=18, maximum_age=50).strftime(constant.DATE_FORMAT))
        if random.randint(0, 1):
            record.add_email(fake.email())
        if random.randint(0, 1):
            record.add_address(fake.street_address() + ', ' + fake.city())
        book.add_record(record)


def populateNotes(notes: NoteBook, quantity):
    print("Populating random notes")
    fake = Faker()
    valid_tags = [item for item in fake.words(nb=20) if len(item) >= 3]
    for _ in range(quantity):
        note = Note(notes.next_id())
        text = ' '.join(fake.words(nb=10))
        note.add_text(text)
        if note.id % 2:
            note.add_tag(fake.word(ext_word_list=valid_tags))
        notes.data[note.id] = note
