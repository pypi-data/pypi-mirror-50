"""Tests the extractor modules in KomiDL"""

import os
import sys
import unittest
from unittest.mock import patch
sys.path.append(os.path.abspath('..'))

from komidl.extractors import get_extractors

class ExtractorTest(unittest.TestCase):
    """Test the extractor modules in KomiDL"""

    def setUp(self):
        self.extractors = get_extractors()

    def _compare_size(self, test, extractor, soup):
        """Compare the expected size from the test dictionary to the actual
        size returned from the extractor implementation"""
        expected_size = test.get('size', None)
        if expected_size is not None:
            actual_size = extractor.get_size(test['url'], soup, None)
            self.assertEquals(expected_size, actual_size)

    def _compare_tags(self, test, extractor, soup):
        """Compare the expected tags from the test dictionary to the actual
        tags returned from the extractor implementation.

        If there exist key-value pairs in the actual implementation not found
        in the expected dictionary for the test, the test will still pass.
        """
        expected_tags = test.get('tags', None)
        if expected_tags is not None:
            actual_tags = extractor.get_tags(test['url'], soup, None)
            # Compare values, flatten potential lists to strings
            for key, value in expected_tags.items():
                expected_str = ''.join(value)
                actual_str = ''.join(actual_tags[key])
                # Normalize the two strings for easy comparison
                expected = sorted(expected_str.upper())
                actual = sorted(actual_str.upper())
                self.assertEquals(expected, actual)

    def _compare_urls(self, test, extractor, soup):
        """Compare the expected URLs from the test dictionary to the actual
        URLs returned from the extractor implementation.

        If there exist image URLs in the actual implementation not found in the
        expected values for the test, the test will still pass.
        """
        expected_imgs = test.get('img_urls', None)
        if expected_imgs is not None:
            actual_imgs = extractor.get_gallery_urls(test['url'], soup, None)
            # It's not expected of the tests to include all URLs and filenames
            # Thus, zip with the expected_imgs as the first arg to iterate
            for expected, (_, actual) in zip(expected_imgs, actual_imgs):
                self.assertEquals(expected, actual)

    def test_extractors(self):
        self.maxDiff = None
        for extractor in self.extractors:
            tests = extractor.get_tests()

            # Skip if no tests
            if not tests:
                continue

            for test in tests:
                url = test.get("url", None)
                # Check that there exists a URL key in the test
                self.assertTrue(url is not None)

                soup = extractor._get_soup(url)

                self._compare_size(test, extractor, soup)
                self._compare_tags(test, extractor, soup)
                self._compare_urls(test, extractor, soup)

if __name__ == "__main__":
    unittest.main()
