# coding: utf8


def left_match(string, match_func, left):
    if string and match_func(string):
        return left(string[1:])


def right_match(string, match_func, right):
    if string and match_func(string):
        return right(string[:-1])


def multi(string, cut):
    result = list()
    while string:
        enum, string = cut(string)
        result.append(enum)
    return result


def choice_one(string, *args):
    return args[0](string) or choice_one(string, *args[1:])


def separate(string, symbol):
    return tuple([enum.strip() for enum in string.split(symbol, 1)])


def fill(enums):
    return enums[0], enums[1] if len(enums) > 1 else ""
