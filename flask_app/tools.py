import re


def check_email_format(string):
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    return re.fullmatch(regex, string)


def check_card_number(string):
    regex = r"(\d{4})(-?)(\d{4})(\2\d{4}){2}"
    return re.match(regex, string)


def check_card_expiry_date(string):
    regex = r"^(0[1-9]|1[0-2])\/?([0-9]{4}|[0-9]{2})$"
    return re.match(regex, string)
