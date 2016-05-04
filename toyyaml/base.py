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
        if value is not None:
            result.append(value)
    return result, string


def multi_string(string, collector, condition):
    result = ""
    while string and condition(string):
        value, string = collector(string)
        result += value
    return result, string


def sequence_string(string, condition=lambda x: True):
    return multi_string(string, unit, condition)

def unit(string):
    def get_unit_string(stream, symbol):
      if stream.startswith(symbol) and not stream.startswith(symbol*2):
          unit_string, tail = multi_string(
              stream[1:],
              lambda x: (x[0], x[1:]),
              lambda x: not (x.startswith(symbol) and not x.startswith(symbol*2))
          )
          return symbol+unit_string+symbol, tail[1:]

    return choice_one(
        string,
        lambda x: get_unit_string(x,  "\""),
        lambda x: get_unit_string(x, "'"),
        lambda x: (x[0], x[1:])
    )


def strip_comment(string):
    if not string or string.startswith(" #"):
        return right(*separate(string, "\n"))
    char, tail = unit(string)
    return char + strip_comment(tail)


def each(func, *args):
    return tuple(func(arg) for arg in args)


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
