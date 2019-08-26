import datetime


def month_of_birthday(date):
    try:
        to_date = datetime.datetime.strptime(date, "%d.%m.%Y")
        return int(to_date.month)
    except Exception as e:
        print(str(e))
        return 0


def current_age(date):
    try:
        to_date = datetime.datetime.strptime(date, "%d.%m.%Y")
        now = datetime.datetime.today()
        return int(now.year - to_date.year)
    except Exception as e:
        print(str(e))
        return -1
