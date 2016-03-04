# coding: utf8

from functools import partial

from .base import multi, left, right, choice_one, separate


def get_enum(string, separate_symbol):
    enum, string = separate(string, separate_symbol)
    return get_value(enum), string


def get_list(string, separate_symbol):
    return multi(string, partial(get_enum, separate_symbol=separate_symbol))


def string_data(string):
    return string.strip()


def list_data(string):
    return get_list(
        left(*separate(
            right(*separate(string, "[")), "]"
        )),
        ","
    )


def get_value(string):
    return choice_one(string, list_data, string_data)
    # if string.startswith("\n"):
    #     return get_pair(string.strip("\n"))
