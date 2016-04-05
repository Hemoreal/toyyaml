# coding: utf8


def left(a, _):
    return a


def right(_, b):
    return b


def none(_):
    return None


def clear_empty_line(string):
    if string.startswith("\n"):
        return clear_empty_line(string[1:])
    if string.lstrip(" ").startswith("\n"):
        return clear_empty_line(string.lstrip(" ")[1:])
    return string


def multi(string, collector, condition=lambda x: True):
    result = list()
    while string and condition(string):
        value, string = collector(string)
        result.append(value)
    return result, string


def choice(condition, a, b):
    return a if condition else b


def choice_one(string, *args):
    return args[0](string) or choice_one(string, *args[1:]) if args else None


def surround(string, start, end):
    return string.startswith(start) and string.endswith(end)


def separate(string, symbol, reverse=False, padding=True):
    result = [enum for enum in choice(reverse, string.rsplit, string.split)(symbol, 1)]
    return fill(result) if padding else result


def fill(enums):
    return enums[0], enums[1] if len(enums) > 1 else ""


def startswith(string, *symbols):
    return string.startswith(symbols[0]) or startswith(string, *symbols[1:]) if symbols else False
