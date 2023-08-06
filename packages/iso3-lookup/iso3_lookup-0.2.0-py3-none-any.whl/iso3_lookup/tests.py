import unittest
from iso3_lookup.lookup import Lookup as L


class MyTest(unittest.TestCase):
    def test1(self):
        self.assertEqual(L.get_country("AFG"), "Afghanistan")

    def test2(self):
        self.assertEqual(L.get_iso3("Albania"), "ALB")

    def test3(self):
        self.assertRaises(ValueError, L.get_iso3, "United Kingdom")