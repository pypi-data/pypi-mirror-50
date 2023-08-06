import unittest
import requests
import json

class TestRequestMethod(unittest.TestCase):

    def test_request(self):
        urlName = "https://google.com"
        self.assertEqual(str(requests.get(urlName)), "<Response [200]>")
 
    def test_synonyms(self, name="ggl"):
        with open('synonyms.json') as f:
            d = json.load(f)
            if name in d.keys():
                name = d[name]
        self.assertEqual(name, "google.com")

if __name__ == '__main__':
    unittest.main()