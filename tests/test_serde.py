# coding=utf-8
import unittest

from messagebird.serde import json_serialize


class TestJSONSerDe(unittest.TestCase):

    def test_tr_check(self):
        self.assertEqual(json_serialize({'body': 'Pijamalı hasta, yağız şoföre çabucak güvendi.'}),
                         """{"body": "Pijamalı hasta, yağız şoföre çabucak güvendi."}""".encode("utf-8"))

    def test_jp_check(self):
        self.assertEqual(json_serialize({'body': 'いろはにほへとちりぬるを'}),
                         """{"body": "いろはにほへとちりぬるを"}""".encode("utf-8"))
