# coding: utf8

from functools import partial

from .base import multi, left_match, right_match, choice_one, fill, separate


def get_enum(string, separate_symbol):
    enum, string = fill(separate(string, separate_symbol))
    return get_value(enum), string


def get_list(string, separate_symbol):
    return multi(
        string,
        partial(get_enum, separate_symbol=separate_symbol),
        partial(right_match, match_func=lambda x: x.endswith("]"))
    )


def string_data(string):
    return string


def list_data(string):
    return left_match(string, lambda x: x.startswith("["), partial(get_list, separate_symbol=","))


def pair_data(string):
    return left_match(string, "")


def get_value(string):
    return choice_one(string, list_data, string_data)
    # if string.startswith("\n"):
    #     return get_pair(string.strip("\n"))
