# coding: utf8

from functools import partial
from .yaml_value import get_enum
from .base import multi, separate


def get_indent(string):
    if string[0] == " ":
        return 1 + get_indent(string[1:])


def equal_indent(a, b):
    return a == b


def get_pair(string):
    key, value = separate(string, ":")
    value, string = pair_value(value)

    return (key, value), string


def pair_value(string):
    return get_enum(string, "\n")


def get_dict(string):
    return multi(string, get_pair, partial(equal_indent, b=get_indent(string)))
