# coding=utf-8
import sys
import unittest

from messagebird.serde import json_serialize


class TestJSONSerDe(unittest.TestCase):

    @staticmethod
    def encode_if_py3(s):
        if sys.version_info > (3, 0):
            return s.encode('utf-8')
        else:
            return s

    def test_tr_check(self):
        self.assertEqual(json_serialize({'body': 'Pijamalı hasta, yağız şoföre çabucak güvendi.'}),
                         self.encode_if_py3("""{"body": "Pijamalı hasta, yağız şoföre çabucak güvendi."}"""))

    def test_jp_check(self):
        self.assertEqual(json_serialize({'body': 'いろはにほへとちりぬるを'}),
                         self.encode_if_py3("""{"body": "いろはにほへとちりぬるを"}"""))
