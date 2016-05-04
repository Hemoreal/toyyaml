# coding: utf8
from .base import multi, surround, choice_one, separate, left, right, each, sequence_string, startswith, unit, strip_comment


def get_enum(string, separate_symbol):
    data, tail = sequence_string(string, lambda x: not x.startswith(separate_symbol))
    return get_value(data), tail[len(separate_symbol):]


def get_list(string, separate_symbol=","):
    return left(*multi(string, lambda x: get_enum(x, separate_symbol)))


def string_value(string):
    string = string.strip()
    return string[1:-1] if surround(string, '"', '"') else string


def list_data(string):
    string = string.strip()
    return get_list(string[1:-1]) if surround(string, "[", "]") else None


def int_data(string):
    try:
        return int(string)
    except ValueError:
        return None


def float_data(string):
    try:
        return float(string)
    except ValueError:
        return None


def empty_data(string):
    return None if string.strip() else ""


def get_value(string):
    return choice_one(strip_comment(string), empty_data, list_data, int_data, float_data, string_value)
