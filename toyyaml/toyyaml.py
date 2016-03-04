# coding: utf8

from functools import partial

from .yaml_value import get_value, string_data
from .base import separate, till, multi, choice, right


def get_indent(string):
    if string and string[0] == " ":
        return 1 + get_indent(string[1:])
    return 0


def equal_indent(a, indent):
    return get_indent(a) == indent


def get_pair(string):
    key, value = separate(string, ":")
    value, string = pair_value(value)
    return (string_data(key), value), string


def pair_value(string):
    enum, r_string = separate(string, "\n")
    if not enum:
        return choice(string.strip().startswith("-"), get_list, get_dict)(r_string)
    return get_value(enum), r_string


def get_list(string):
    def collect(stream):
        result, stream = separate(right(*separate(stream, "-")), "\n")
        return get_value(result), stream

    enum, string = till(string, collect, partial(equal_indent, indent=get_indent(string)))
    return enum, string


def get_dict(string):
    enum, string = till(string, get_pair, partial(equal_indent, indent=get_indent(string)))
    return dict(enum), string


def load(string):
    return dict(multi(string, get_pair))
