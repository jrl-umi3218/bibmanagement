# Copyright 2019-2022 CNRS-AIST JRL

from bibmanagement.check import LevenshteinDistance
import unittest

class TestLevenshteinDistance(unittest.TestCase):
    def test_distance(self):
        w1 = 'qwerty'
        w2 = 'azerty'
        w3 = 'wert'
        w4 = 'qwertyu'
        w5 = 'qewrty'
        
        self.assertEqual(LevenshteinDistance.distance(w1, w1), 0)
        self.assertEqual(LevenshteinDistance.distance(w1, w2), 2)
        self.assertEqual(LevenshteinDistance.distance(w1, w3), 2)
        self.assertEqual(LevenshteinDistance.distance(w1, w4), 1)
        self.assertEqual(LevenshteinDistance.distance(w1, w5), 2)
        
        self.assertEqual(LevenshteinDistance.distance(w2, w1), 2)
        self.assertEqual(LevenshteinDistance.distance(w2, w2), 0)
        self.assertEqual(LevenshteinDistance.distance(w2, w3), 3)
        self.assertEqual(LevenshteinDistance.distance(w2, w4), 3)
        self.assertEqual(LevenshteinDistance.distance(w2, w5), 3)
        
        self.assertEqual(LevenshteinDistance.distance(w3, w1), 2)
        self.assertEqual(LevenshteinDistance.distance(w3, w2), 3)
        self.assertEqual(LevenshteinDistance.distance(w3, w3), 0)
        self.assertEqual(LevenshteinDistance.distance(w3, w4), 3)
        self.assertEqual(LevenshteinDistance.distance(w3, w5), 3)
        
        self.assertEqual(LevenshteinDistance.distance(w4, w1), 1)
        self.assertEqual(LevenshteinDistance.distance(w4, w2), 3)
        self.assertEqual(LevenshteinDistance.distance(w4, w3), 3)
        self.assertEqual(LevenshteinDistance.distance(w4, w4), 0)
        self.assertEqual(LevenshteinDistance.distance(w4, w5), 3)
        
        self.assertEqual(LevenshteinDistance.distance(w5, w1), 2)
        self.assertEqual(LevenshteinDistance.distance(w5, w2), 3)
        self.assertEqual(LevenshteinDistance.distance(w5, w3), 3)
        self.assertEqual(LevenshteinDistance.distance(w5, w4), 3)
        self.assertEqual(LevenshteinDistance.distance(w5, w5), 0)

if __name__ == '__main__':
    unittest.main()