# coding: utf8

from functools import partial

from .yaml_value import get_value, string_data
from .base import separate, till, multi, choice, right, empty, choice_one


def get_indent(string):
    if string and string[0] == " ":
        return 1 + get_indent(string[1:])
    return 0


def equal_indent(a, indent):
    return get_indent(a) == indent


def split_line(row):
    return row.startswith("---")


def remove_comment(string):
    return "\n".join([row for row in string.split("\n") if row and row.lstrip() and not split_line(row)])


def get_pair(string):
    key, value = separate(string, ":")
    value, string = pair_value(value)
    return (string_data(key), value), string


def pair_value(string):
    enum, r_string = separate(string, "\n")
    if not enum:
        return choice(string.strip().startswith("-"), get_list, get_dict)(r_string)
    if enum.strip() in ("|", ">"):
        return multi_string_data(r_string)
    return get_value(enum), r_string


def multi_string_data(string):
    def collector(stream):
        value, stream = separate(stream, "\n")
        return string_data(value), stream
    result, tail = till(string, collector, partial(equal_indent, indent=get_indent(string)))
    return "\n".join(result).rstrip(), tail


def pair_data(string):
    line, tail = separate(string, "\n")
    if line.strip().endswith(":"):
        return get_pair(string)
    if line.find(": ") != -1:
        return get_pair(string)
    return None


def list_data(string):
    result = choice(string.strip().startswith("-"), get_list, empty)(string)
    return result[0] if result else None


def get_list(string):
    def collector(stream):
        result, stream = separate(right(*separate(stream, "-")), "\n")
        return get_value(result), stream
    return till(string, collector, partial(equal_indent, indent=get_indent(string)))


def get_dict(string):
    enum, string = till(string, pair_data, partial(equal_indent, indent=get_indent(string)))
    return dict(enum), string


def load(string):
    string = remove_comment(string)
    return choice_one(string, lambda x: list_data(x), lambda x: dict(multi(x, pair_data)))
