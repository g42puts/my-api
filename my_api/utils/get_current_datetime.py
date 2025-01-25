from datetime import datetime


def get_current_datetime_formatted():
    return datetime.now().strftime(format='%m/%d/%Y, %H:%M:%S')
