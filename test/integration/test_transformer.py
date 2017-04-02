import unittest
from xml.etree import ElementTree as ET
from xmlcomparer import transformer

import logging
#logging.basicConfig(level=logging.DEBUG)


class TestTransformer(unittest.TestCase):
    def test_can_ignore_order(self):
        xml_incorrect_order = ET.parse("../../demo/sort_only2.xml")
        t = transformer.Transformer(xml_incorrect_order)
        t.ignore_tag_order(".*")
        xml_incorrect_order_transformed = t.transform()
        xml_correct_order = ET.parse("../../demo/sort_only1.xml")

        print("--- correct")
        print(ET.tostring(xml_correct_order.getroot(), encoding="unicode"))
        print("--- incorrect")
        print(ET.tostring(xml_incorrect_order.getroot(), encoding="unicode"))
        print("--- transformed")
        print(ET.tostring(xml_incorrect_order_transformed.getroot(), encoding="unicode"))


