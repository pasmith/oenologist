import unittest
from utils.geocode_utils import get_country_code as lookup


class CountryCodeLookupTest(unittest.TestCase):
    def test_lookup_valid_country(self):
        self.assertEqual(lookup("France"), "FR")
        self.assertEqual(lookup("United States Of America"), "US")

    def test_lookup_unknown_country(self):
        self.assertIsNone(lookup("United States"))

    def test_overrides(self):
        self.assertEqual(lookup("US"), "US")


if __name__ == "__main__":
    unittest.main()
