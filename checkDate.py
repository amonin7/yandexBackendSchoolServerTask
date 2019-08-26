import datetime


def check_date(date):
    try:
        to_date = datetime.datetime.strptime(date, "%d.%m.%Y")
        now = datetime.datetime.today()

        return int(now > to_date)
    except Exception as e:
        print(str(e))
        return 0
