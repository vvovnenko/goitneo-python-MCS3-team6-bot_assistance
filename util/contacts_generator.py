import constant
from faker import Faker
from contacts import Record


def populateAddressBook(book, quantity):
    print("Populating random contact data")
    fake = Faker()

    for _ in range(quantity):
        record = Record(fake.first_name())
        record.add_phone(str(fake.random_number(digits=10, fix_len=True)))
        record.add_birthday(fake.date_of_birth(
            minimum_age=18, maximum_age=50).strftime(constant.DATE_FORMAT))
        book.add_record(record)
