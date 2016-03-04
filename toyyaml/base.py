# coding: utf8


def left(a, _):
    return a


def right(_, b):
    return b


def multi(string, cut):
    result = list()
    while string:
        enum, string = cut(string)
        result.append(enum)
    return result


def choice(condition, a, b):
    return a if condition else b


def choice_one(string, *args):
    return args[0](string) or choice_one(string, *args[1:])


def separate(string, symbol, reverse=False, padding=True):
    result = [enum for enum in choice(reverse, string.rsplit, string.split)(symbol, 1)]
    return fill(result) if padding else result


def fill(enums):
    return enums[0], enums[1] if len(enums) > 1 else ""
