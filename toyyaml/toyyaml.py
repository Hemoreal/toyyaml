# coding: utf8

from .base import separate, choice_one, choice, right, left, startswith, none, multi, sequence_string, strip_comment
from .yaml_value import get_value, string_value


def get_indent(string):
    return len(string) - len(string.lstrip(" "))



def equal_indent(a, indent):
    return get_indent(a) == indent


def multi_string_data(string):
    if startswith(string.lstrip(" "), "|", ">"):
        string = right(*separate(string, "\n"))
        strings, tail = multi(
            string,
            lambda x: separate(x, "\n"),
            lambda x: x.lstrip(" ").startswith("\n") or equal_indent(x, get_indent(string))
        )
        return "\n".join([data.strip() for data in strings]), tail


def pair_with_simple_data_value(string):
    def _get_pair(stream):
        head, tail = separate(stream, ": ")
        value, tail = get_data(tail)
        return (get_value(head), value), tail

    return choice(separate(string, "\n")[0].find(": ") != -1, _get_pair, none)(string)


def pair_with_complicate_data_value(string):
    def _get_pair(stream):
        index = left(*separate(stream, "\n")).rfind(":")
        value, tail = get_data(stream[index+1:])
        return (get_value(stream[:index]), value), tail

    return choice(separate(string, "\n")[0].strip().endswith(":"), _get_pair, none)(string)


def pair_data(string):
    return choice_one(string.lstrip(), pair_with_complicate_data_value, pair_with_simple_data_value)


def list_enum(string):
    string = string.lstrip()
    if startswith(string, "- ", "-\n"):
        return get_data(string[1:])


def get_data(string):
    return choice_one(string, comment_data, list_data, dict_data, multi_string_data, mapping_data, simple_data)


def list_data(string):
    if startswith(string.lstrip(), "- ", "-\n"):
        string = string.lstrip("\n")
        data, tail = multi(
            string,
            list_enum,
            lambda x: equal_indent(x.lstrip("\n"), get_indent(string)) and startswith(x.lstrip(), "- ", "-\n")
        )
        return (data, tail) if data else None


def dict_data(string):
    if string.startswith("\n"):
        string = right(*separate(string, "\n"))
        data, tail = multi(string, pair_data, lambda x: equal_indent(string.lstrip("\n"), get_indent(x)))
        return (dict(data), tail) if data else None


def mapping_enums(string):
    key, tail = sequence_string(string.lstrip(","), lambda x: not x.startswith(": "))
    value, tail = sequence_string(tail[2:], lambda x: not startswith(x, ", ", ",\n", "}"))
    return (get_value(key), get_value(value)), tail


def mapping_data(string):
    if string.lstrip(" ").startswith("{"):
        string = right(*separate(string, "{"))
        data, tail = multi(string, mapping_enums, lambda x: not x.startswith("}"))
        return dict(data), tail[1:]

def simple_data(string):
    data, tail = separate(string, "\n")
    return get_value(data), tail


def get_structure(string):
    result =  choice_one(string, comment_data, stream_start, list_enum, pair_data)
    return result


def comment_data(string):
    if string.lstrip().startswith("# "):
        return None, right(*separate(string, "\n"))


def stream_start(string):
    if string.startswith("---"):
        def comment(stream):
            return multi_string_data(stream) or separate(stream, "\n")

        return choice_one(right(*comment(string[3:])), list_data, dict_data)


def stream_end(string):
    if string.startswith("..."):
        _, tail = separate(string, "\n")
        return None, tail


def loads(string):
    result = left(*multi(string, get_structure))
    if len(result) == 1:
        result = result[0]
    try:
        return dict(result)
    except Exception:
        return result


def load(file_obj):
    with open(file_obj, "r") as f:
        string = f.read()
    return loads(string)
