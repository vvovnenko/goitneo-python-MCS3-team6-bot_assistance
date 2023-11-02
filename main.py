from birthdays import date_birthday, show_birthday_n_days
from storage import StorageContext, NotesStorageStrategy, ContactsStorageStrategy
from exceptions import ValidationException, BotSyntaxException, DuplicateException, NotFoundException
from contacts import AddressBook, Record
from notes import NoteBook


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
        except (ValidationException, DuplicateException, NotFoundException) as e:
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


# note command handlers - move to separate class


@input_error
def add_note(notes: NoteBook):
    note = notes.add_note()
    text = input("Enter note text: ")
    note.add_text(text)
    return f"Note [{note.id}] created."


@input_error
def edit_note(args, notes: NoteBook):
    if len(args) == 0:
        raise BotSyntaxException(get_syntax_error_message("edit-note [id]"))
    note = notes.find(args[0])
    text = input("Enter new text: ")
    note.add_text(text)
    return f"Note [{note.id}] updated."


@input_error
def delete_note(args, notes: NoteBook):
    if len(args) == 0:
        raise BotSyntaxException(
            get_syntax_error_message("delete-note [id]"))
    id = args[0]
    notes.delete_note(args[0])
    return f"Note [{id}] deleted."


@input_error
def show_notes(notes: NoteBook):
    return "\n".join([f"{note}" for note in notes.values()])


@input_error
def get_note(args, notes: NoteBook):
    if not args:
        raise BotSyntaxException(get_syntax_error_message("note [id]"))
    note = notes.find(args[0])
    return f"id: {note.id}\ntext: {note.text}"


@input_error
def search_notes(args, notes: NoteBook):
    if not args:
        raise BotSyntaxException(get_syntax_error_message(
            "search-notes [search-string]"))
    if args[0] == '-tag':
        if len(args) < 2:
            raise BotSyntaxException(
                get_syntax_error_message("search-notes -tag [tag]"))
        search_tags = args[1:]
        result = notes.search_by_tags(search_tags)
    else:
        result = notes.search(args)

    return "\n".join(str(note) for note in result) if result else "Nothing found"


@input_error
def add_note_tag(args, notes: NoteBook):
    try:
        id, tag = args
    except:
        raise BotSyntaxException(
            get_syntax_error_message("tag-note [id] [tag]"))

    note = notes.find(id)
    note.add_tag(tag)
    return f"Tag #{tag} added to note {note.id}"
# note command handlers - move to separate class


@input_error
def search_contacts(args: list, contacts: AddressBook):
    word, = args
    if len(word) < 2:
        raise BotSyntaxException(
            'The search word must consist of at least 2 characters')

    return "\n".join([str(record) for record in contacts.search(word)])

@input_error
def remove_contact(args, contacts):
    name = args[0]
    record = contacts.find(name)
    if record:
        contacts.delete(name)
        return f"Contact {name} removed from Address Book!"
    else:
        raise KeyError


def get_syntax_error_message(expected_command):
    return f'Incorrect syntax, enter command in the following format: "{expected_command}"'


def start_bot(contacts: AddressBook, notes: NoteBook):
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
        elif command == "bd":
            print(show_birthday_n_days(contacts, *args))
        elif command == "bdate":
            print(date_birthday(contacts, *args))
        elif command == "del":
            print(remove_contact(args, contacts)) 
        # Note commands - move to separate handler
        elif command == "note":
            print(get_note(args, notes))
        elif command == "add-note":
            print(add_note(notes))
        elif command == "edit-note":
            print(edit_note(args, notes))
        elif command == "delete-note":
            print(delete_note(args, notes))
        elif command == "tag-note":
            print(add_note_tag(args, notes))
        elif command == "note":
            print(get_note(args, notes))
        elif command == "search-notes":
            print(search_notes(args, notes))
        elif command == "all-notes":
            print(show_notes(notes))
        # Note commands - move to separate handler
        elif command == "search":
            print(search_contacts(args, contacts))

        else:
            print("Invalid command.")


def main():
    contacts_storage = StorageContext(ContactsStorageStrategy())
    notes_storage = StorageContext(NotesStorageStrategy())

    contacts = AddressBook()
    notes = NoteBook()

    # Load data from file
    contacts = contacts_storage.load_from_file(contacts)
    notes = notes_storage.load_from_file(notes)

    start_bot(contacts, notes)

    # Save data to file
    contacts_storage.save_to_file(contacts)
    notes_storage.save_to_file(notes)


if __name__ == "__main__":
    main()
