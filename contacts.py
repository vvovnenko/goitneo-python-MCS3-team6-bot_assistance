import constant
from collections import UserDict
from exceptions import ValidationException, DuplicateException, NotFoundException, NotFoundException
from datetime import datetime
from birthdays import get_birthdays_per_week


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        try:
            birthday = datetime.strptime(
                new_value, constant.DATE_FORMAT).date()
        except ValueError:
            raise ValidationException(
                'Birthday should be in "DD.MM.YYYY" format')
        self._value = birthday


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if not (len(new_value) == constant.PHONE_LEN and new_value.isdigit()):
            raise ValidationException(
                f"Phone must contain {constant.PHONE_LEN} digits")
        self._value = new_value


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.birthday = None
        self.phones = []

    def add_phone(self, phone):
        phones = [phone.value for phone in self.phones]
        if phone in phones:
            raise DuplicateException("Phone already exists")
        self.phones.append(Phone(phone))

    def find_phone(self, phone):
        return next((p for p in self.phones if p.value == phone), None)

    def edit_phone(self, old, new):
        existing_phone = self.find_phone(old)
        if not existing_phone:
            error_msg = f"Phone {old} number not found for record {self.name}"
            raise NotFoundException(error_msg)

        existing_phone.value = new

    def remove_phone(self, phone):
        existing_phone = self.find_phone(phone)
        if existing_phone:
            self.phones.remove(existing_phone)

    def add_birthday(self, date):
        self.birthday = Birthday(date)

    def get_birthday(self):
        return self.birthday.value if self.birthday else None

    def __str__(self):
        return f"Contact name: {self.name.value:15} | Birthday: {str(self.get_birthday()):^10} | Phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        key = record.name.value
        self.data[key] = record

    def find(self, name):
        try:
            return self.data[name]
        except KeyError:
            raise NotFoundException("Contact is not found")

    def delete(self, name):
        self.data.pop(name)

    def get_birthdays_per_week(self):
        return get_birthdays_per_week(self.data)
