import storage
from exceptions import ValidationException, BotSyntaxException, DuplicateException, NotFoundException
from contacts import AddressBook, Record


def parse_input(user_input):
    try:
        cmd, *args = user_input.split()
    except:
        return "Invalid command."
    cmd = cmd.strip().lower()
    return cmd, *args


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValidationException, DuplicateException, NotFoundException, ) as e:
            return e
        except BotSyntaxException as e:
            return e
    return inner


@input_error
def add_contact(args, contacts: AddressBook):
    try:
        name, phone = args
    except:
        raise BotSyntaxException(
            get_syntax_error_message("add [name] [phone]"))
    try:
        existing_record = contacts.find(name)
        existing_record.add_phone(phone)
    except NotFoundException:
        record = Record(name)
        record.add_phone(phone)
        contacts.add_record(record)
    return "Contact added."


@input_error
def change_contact(args, contacts: AddressBook):
    try:
        name, old_phone, new_phone = args
    except:
        raise BotSyntaxException(
            get_syntax_error_message("change [name] [old_phone] [new_phone]"))
    found_contact = contacts.find(name)
    if found_contact:
        found_contact.edit_phone(old_phone, new_phone)
        return "Contact changed."


@input_error
def get_phone(args, contacts: AddressBook):
    if len(args) == 0:
        raise BotSyntaxException(get_syntax_error_message("phone [name]"))

    return "; ".join(map(str, contacts.find(args[0]).phones))


@input_error
def add_birthday(args, contacts: AddressBook):
    try:
        name, birthday = args
    except:
        raise BotSyntaxException(
            get_syntax_error_message("add-birthday [name] [birthday]"))
    found_contact = contacts.find(name)
    if found_contact:
        found_contact.add_birthday(birthday)
        return "Birthday added."


@input_error
def show_birthday(args, contacts: AddressBook):
    if len(args) == 0:
        raise BotSyntaxException(
            get_syntax_error_message("show-birthday [name]"))
    return contacts.find(args[0]).get_birthday()


@input_error
def show_birthdays_next_week(contacts: AddressBook):
    birthdays_per_weekday = contacts.get_birthdays_per_week()
    result = []
    for weekday, contacts in birthdays_per_weekday.items():
        names = ', '.join(contact.name.value for contact in contacts)
        result.append(f"{weekday}: {names}")

    return "\n".join(result)


@input_error
def show_all_contacts(contacts):
    return "\n".join([f"{record}" for record in contacts.values()])


def get_syntax_error_message(expected_command):
    return f'Incorrect syntax, enter command in the following format: "{expected_command}"'


def start_bot(contacts):
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(get_phone(args, contacts))
        elif command == "all":
            print(show_all_contacts(contacts))
        elif command == "add-birthday":
            print(add_birthday(args, contacts))
        elif command == "show-birthday":
            print(show_birthday(args, contacts))
        elif command == "birthdays":
            print(show_birthdays_next_week(contacts))
        else:
            print("Invalid command.")


def main():
    contacts = AddressBook()

    # Load data from file or generate random contacts
    contacts = storage.load_contacts_from_file(contacts)

    start_bot(contacts)

    # Save contacts to file
    storage.save_contacts_to_file(contacts)


if __name__ == "__main__":
    main()
