# coding: utf8

from functools import partial

from .base import multi, surround, choice_one, separate, left


def get_enum(string, separate_symbol):
    enum, string = separate(string, separate_symbol)
    return get_value(enum), string


def get_list(string, separate_symbol=","):
    return left(*multi(string, partial(get_enum, separate_symbol=separate_symbol)))


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


def strip_comment(string):
    if not string or string.startswith(" #"):
        return ""
    if string.startswith("\""):
        data, tail = separate(string[1:], "\"")
        return "\"" + data + "\"" + strip_comment(tail)
    return string[0] + strip_comment(string[1:])


def get_value(string):
    return choice_one(strip_comment(string), empty_data, list_data, int_data, float_data, string_value)
