import datetime


def convert_str_to_date_object(date_: str) -> datetime:
    day, month, year = date_.split('.')
    correct_format = f'{year}-{month}-{day}'
    date_obj = datetime.date.fromisoformat(correct_format)
    return date_obj
