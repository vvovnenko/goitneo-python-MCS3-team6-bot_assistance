from datetime import datetime


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
