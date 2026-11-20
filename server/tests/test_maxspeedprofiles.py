"""Country-specific CIS speed profiles and OSM maxspeed symbols."""
import os
import sys
import unittest
from types import SimpleNamespace

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import maxspeedprofiles  # noqa: E402


class SymbolicTags(unittest.TestCase):
    def test_all_twelve_countries_have_explicit_urban_rural_and_motorway_values(self):
        self.assertEqual(maxspeedprofiles.COUNTRIES, frozenset(
            ("AM", "AZ", "BY", "GE", "KG", "KZ", "MD", "RU", "TJ", "TM", "UA", "UZ")))
        for country in maxspeedprofiles.COUNTRIES:
            with self.subTest(country=country):
                self.assertIsInstance(maxspeedprofiles.resolve_tag(f"{country}:urban"), int)
                self.assertIsInstance(maxspeedprofiles.resolve_tag(f"{country}:rural"), int)
                self.assertIsInstance(maxspeedprofiles.resolve_tag(f"{country}:motorway"), int)

    def test_russian_rural_is_90_and_legacy_transposition_is_accepted(self):
        self.assertEqual(maxspeedprofiles.resolve_tag("RU:rural"), 90)
        self.assertEqual(maxspeedprofiles.resolve_tag("ru:rual"), 90)

    def test_country_specific_values_differ(self):
        self.assertEqual(maxspeedprofiles.resolve_tag("BY:motorway"), 120)
        self.assertEqual(maxspeedprofiles.resolve_tag("KZ:motorway"), 140)
        self.assertEqual(maxspeedprofiles.resolve_tag("UA:motorway"), 130)
        self.assertEqual(maxspeedprofiles.resolve_tag("UZ:rural"), 100)
        self.assertEqual(maxspeedprofiles.resolve_tag("MD:urban"), 50)
        self.assertEqual(maxspeedprofiles.resolve_tag("AZ:urban"), 60)
        self.assertEqual(maxspeedprofiles.resolve_tag("AZ:rural"), 90)
        self.assertEqual(maxspeedprofiles.resolve_tag("UA:trunk"), 110)
        self.assertEqual(maxspeedprofiles.resolve_tag("UZ:living_street"), 30)

    def test_unknown_values_are_not_guessed(self):
        for value in (None, "", "90", "RU:unknown", "XX:rural", "RU:rualish", "RU:rural;RU:urban"):
            with self.subTest(value=value):
                self.assertIsNone(maxspeedprofiles.resolve_tag(value))


class DefaultProfiles(unittest.TestCase):
    @staticmethod
    def spec(cls="trunk", urban=False, oneway=False, lanes=None):
        return SimpleNamespace(cls=cls, urban=urban, oneway=oneway, lanes=lanes)

    def test_rural_trunk_defaults_are_country_specific(self):
        expected = {"RU": 90, "BY": 90, "UA": 90, "KZ": 100, "UZ": 100, "MD": 90, "AZ": 90}
        for country, value in expected.items():
            with self.subTest(country=country):
                self.assertEqual(maxspeedprofiles.default_kmh(country, self.spec()), value)

    def test_divided_road_exceptions(self):
        divided = self.spec("trunk", oneway=True, lanes=2)
        self.assertEqual(maxspeedprofiles.default_kmh("KZ", divided), 110)
        self.assertEqual(maxspeedprofiles.default_kmh("UA", divided), 110)
        self.assertEqual(maxspeedprofiles.default_kmh("RU", divided), 90)
        primary_divided = self.spec("primary", oneway=True, lanes=2)
        self.assertEqual(maxspeedprofiles.default_kmh("KZ", primary_divided), 110)
        self.assertEqual(maxspeedprofiles.default_kmh("UA", primary_divided), 110)

    def test_urban_motorway_and_living_street(self):
        self.assertEqual(maxspeedprofiles.default_kmh("RU", self.spec("primary", urban=True)), 60)
        self.assertEqual(maxspeedprofiles.default_kmh("UZ", self.spec("primary", urban=True)), 70)
        self.assertEqual(maxspeedprofiles.default_kmh("AZ", self.spec("primary", urban=True)), 60)
        self.assertEqual(maxspeedprofiles.default_kmh("AZ", self.spec("unclassified")), 90)
        self.assertEqual(maxspeedprofiles.default_kmh("UZ", self.spec("living_street", urban=True)), 30)
        self.assertEqual(maxspeedprofiles.default_kmh("RU", self.spec("motorway")), 110)
        self.assertEqual(maxspeedprofiles.default_kmh("KZ", self.spec("motorway")), 140)
        self.assertEqual(maxspeedprofiles.default_kmh("BY", self.spec("motorway")), 120)
        self.assertEqual(maxspeedprofiles.default_kmh("RU", self.spec("living_street", urban=True)), 20)

    def test_unknown_country_keeps_existing_fallback(self):
        self.assertIsNone(maxspeedprofiles.default_kmh("US", self.spec()))
        self.assertIsNone(maxspeedprofiles.default_kmh(None, self.spec()))


if __name__ == "__main__":
    unittest.main()
