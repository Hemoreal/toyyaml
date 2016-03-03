# coding: utf8


def left_match(string, match_func, left):
    if string and match_func(string):
        return left(string[1:])


def right_match(string, match_func):
    if string and match_func(string):
        return string[:-1]


def multi(string, func, rest):
    result = list()
    enum, string = func(string)
    while not rest(enum):
        print "mutli:", enum
        result.append(enum)
        enum, string = func(string)
    return result + [rest(enum)]


def choice_one(string, *args):
    return args[0](string) or choice_one(string, *args[1:])


def separate(string, symbol):
    return tuple([enum.strip() for enum in string.split(symbol, 1)])


def fill(enums):
    return enums[0], enums[1] if len(enums) > 1 else ""
