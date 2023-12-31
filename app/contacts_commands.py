from app.command_handler import command
from app.contacts import Record
from app.storage import storage
from app.exceptions import BotSyntaxException, NotFoundException
from datetime import date, datetime
from app.constant import DATE_FORMAT


@command(name='add')
def add_contact(args):
    """Create new contact in the book with a phone, or add a phone to existent  
    usage:
        add [contact_name] [phone]
    arguments:
        contact_name - name of contact
        phone - phone number, 10 digits (example 0991911155)
    """
    contacts = storage.contacts
    try:
        name, phone = args
    except Exception:
        raise BotSyntaxException()
    try:
        existing_record = contacts.find(name)
        existing_record.add_phone(phone)
    except NotFoundException:
        record = Record(name)
        record.add_phone(phone)
        contacts.add_record(record)
    return "Contact added."


@command(name='change-phone')
def change_contact_phone(args):
    """Change contact phone
    usage:
        change-phone [contact_name] [old_phone] [new_phone]
    arguments:
        contact_name - name of contact
        old_phone - contact phone number
        new_phone - new contact phone number, 10 digits (example 0991911155)
    """
    contacts = storage.contacts
    try:
        name, old_phone, new_phone = args
    except Exception:
        raise BotSyntaxException()
    found_contact = contacts.find(name)
    if found_contact:
        found_contact.edit_phone(old_phone, new_phone)
        return "Contact changed."


@command(name='phone')
def get_phone(args):
    """Show contact phone
    usage:
        phone [contact_name] [phone]
    arguments:
        contact_name - name of contact
        phone - phone number, 10 digits (example 0991911155)
    """
    contacts = storage.contacts
    if len(args) == 0:
        raise BotSyntaxException()

    return "; ".join(map(str, contacts.find(args[0]).phones))


@command(name='add-birthday')
def add_birthday(args):
    """Add contact birthday
    usage:
        add-birthday [contact_name] [birthdate]
    arguments:
        contact_name - name of contact
        birthdate - contact birthdate (example 19.07.1999)
    """
    contacts = storage.contacts
    try:
        name, birthday = args
    except Exception:
        raise BotSyntaxException()
    found_contact = contacts.find(name)
    if found_contact:
        found_contact.add_birthday(birthday)
        return "Birthday added."


@command(name='show-birthday')
def show_birthday(args):
    """Show contact birthday
    usage:
        show-birthday [contact_name]
    arguments:
        contact_name - name of contact
    """
    contacts = storage.contacts
    if len(args) == 0:
        raise BotSyntaxException()
    return contacts.find(args[0]).get_birthday()


@command(name='all-contacts')
def show_all_contacts(args):
    """Show all contacts
    usage:
        all-contacts
    """
    contacts = storage.contacts

    return ''.join([f"{record}" for record in contacts.values()])


@command(name='del-contact')
def remove_contact(args):
    """Delete contact
    usage:
        del-contact [contact_name]
    arguments:
        contact_name - name of contact
    """
    contacts = storage.contacts
    if not args:
        raise BotSyntaxException()
    name = args[0]
    record = contacts.find(name)
    if record:
        contacts.delete(name)
        return f"Contact {name} removed from Address Book!"
    else:
        raise KeyError


@command('search-contacts')
def search_contacts(args: list):
    """Search contacts on all the fields
    usage:
        search-contacts [word]
    arguments:
        word - search word min 2 characters length
    """
    contacts = storage.contacts
    word, = args
    if len(word) < 2:
        raise BotSyntaxException()

    result = contacts.search(word)
    return "".join([str(record) for record in result]) if result else "Nothing found."


@command(name='birthdays')
def show_birthdays_next_week(args):
    """Show all birthdays in a week period
    usage:
        birthdays
    """
    contacts = storage.contacts
    birthdays_per_weekday = contacts.get_birthdays_per_week()
    result = []
    for weekday, contacts in birthdays_per_weekday.items():
        names = ', '.join(contact.name.value for contact in contacts)
        result.append(f"{weekday}: {names}")

    return "\n".join(result)


@command(name='birthdays-in-days')
def show_birthday_n_days(args):
    """Show contacts with birthday in N days
    usage:
        birthdays-in-days [days]
    arguments:
        days - number of days
    """
    contacts = storage.contacts
    if args and args[0].isdigit():
        days = int(args[0])
        result = f'List of users with birthday in {days} days:\n'
        print_list = [contact for contact in contacts.values() if contact.days_to_birthday(contact.birthday) == days]
        for item in print_list:
            result += f'{item.name} date born {item.birthday}\n'
        return result if print_list else f'No birthdays in {days} days'
    else:
        return "Invalid input. Please provide a valid number of days."


@command(name='birthdays-by-date')
def date_birthday(args):
    """Show contacts with birthday by date
    usage:
        birthdays-by-date [date]
    arguments:
        date - a date in 'DD.MM' format (example 02.11)
    """
    contacts = storage.contacts
    if len(args) < 1:
        return "Invalid input. Please provide a specific date."

    try:
        specific_date = datetime.strptime(args[0], '%d.%m').date().replace(year=date.today().year)
    except ValueError:
        return "Invalid date format. Please provide a date in 'DD.MM' format."

    birthday_contacts = [
        contact for contact in contacts.values() if contact.birthday and
                                                    contact.birthday.value.day == specific_date.day and
                                                    contact.birthday.value.month == specific_date.month]

    if birthday_contacts:
        result = f"List of contacts with birthday on {specific_date}:\n"
        for contact in birthday_contacts:
            result += f" Contact : {contact.name.value} date born : {contact.birthday.value.strftime(DATE_FORMAT)}\n"
        return result
    else:
        return f"No contacts with birthday on {specific_date}."


@command(name='add-email')
def add_email(args):
    """Add contact email
        usage:
            add-email [contact_name] [email]
        arguments:
            contact_name - name of contact
            email - valid email address
        """
    try:
        name, email = args
    except Exception:
        raise BotSyntaxException()
    contacts = storage.contacts
    found_contact = contacts.find(name)
    if found_contact:
        found_contact.add_email(email)
        return "Email added."


@command(name='add-ad')
def add_address(args):
    """Add contact address
        usage:
            add-ad [contact_name] [address]
        arguments:
            contact_name - name of contact
            address - contact address, e.g. "221B Baker Street"
        """
    try:
        name = args[0]
        address = ' '.join(args[1:]).strip()
    except Exception:
        raise BotSyntaxException()
    if address:
        record = storage.contacts.find(name)
        if record:
            record.add_address(address)
            return f"Address added to contact {name}"
        else:
            raise BotSyntaxException()
    else:
        raise BotSyntaxException()
