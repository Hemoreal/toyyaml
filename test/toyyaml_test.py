# coding: utf8

import unittest

from toyyaml.toyyaml import get_pair


class TestYaml(unittest.TestCase):
    def test_get_pair_with_simple_dict(self):
        pair, string = get_pair("aaa: bbb")
        self.assertEquals(pair, ("aaa", "bbb"))
        self.assertEquals(string, "")

    def test_get_pair_and_popup_string(self):
        pair, string = get_pair("aaa: bbb\nasdasd")
        self.assertEquals(pair, ("aaa", "bbb"))
        self.assertEquals(string, "asdasd")

    def test_get_pair_with_value_is_list(self):
        pair, string = get_pair("aaa: [bb, cc, dd]")

        self.assertEquals(pair, ("aaa", ["bb", "cc", "dd"]))
        self.assertEquals(string, "")
