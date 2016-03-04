# coding: utf8

import unittest

from toyyaml.yaml_value import get_enum


class TestYamlValue(unittest.TestCase):
    def test_get_simple_enum(self):
        enum, string = get_enum("aaa", ",")
        self.assertEquals(enum, "aaa")
        self.assertEquals(string, "")

    def test_get_enum_split_by_comma(self):
        enum, string = get_enum("aaa, aaa", ",")
        self.assertEquals(enum, "aaa")
        self.assertEquals(string, " aaa")
