from datetime import date, datetime

from constant import DATE_FORMAT


def get_birthdays_per_week(users_list):
    congrats_per_day = {
        "Monday": [],
        "Tuesday": [],
        "Wednesday": [],
        "Thursday": [],
        "Friday": [],
    }

    today = datetime.today().date()

    for record in [r for r in users_list.values() if r.get_birthday()]:
        birthday_this_year = get_birthday_this_year(
            today, record.get_birthday())

        delta_days = (birthday_this_year - today).days

        if delta_days < 7:
            if birthday_this_year.weekday() == 1:
                congrats_per_day["Tuesday"].append(record)
            elif birthday_this_year.weekday() == 2:
                congrats_per_day["Wednesday"].append(record)
            elif birthday_this_year.weekday() == 3:
                congrats_per_day["Thursday"].append(record)
            elif birthday_this_year.weekday() == 4:
                congrats_per_day["Friday"].append(record)
            else:
                congrats_per_day["Monday"].append(record)

    return congrats_per_day


def get_birthday_this_year(today, birthday):
    try:
        birthday_this_year = birthday.replace(year=today.year)
    # handle leap year exception
    except ValueError:
        birthday_this_year = birthday.replace(day=birthday.day - 1)
        birthday_this_year = birthday_this_year.replace(year=today.year)

    if birthday_this_year < today:
        birthday_this_year = birthday.replace(year=today.year + 1)
    return birthday_this_year


def show_birthday_n_days(contacts, *args):
    if args and args[0].isdigit():
        days = int(args[0])
        result = f'List of users with birthday in {days} days:\n'
        print_list = [contact for contact in contacts.values() if contact.days_to_birthday(contact.birthday) == days]
        for item in print_list:
            result += f'{item.name} date born {item.birthday}\n'
        return result
    else:
        return "Invalid input. Please provide a valid number of days."
    
    
def date_birthday(contacts, *args):
    if len(args) < 1:
        return "Invalid input. Please provide a specific date."

    try:
        specific_date = datetime.strptime(args[0], '%d.%m').date().replace(year=date.today().year)
    except ValueError:
        return "Invalid date format. Please provide a date in 'DD.MM' format."

    birthday_contacts =[
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