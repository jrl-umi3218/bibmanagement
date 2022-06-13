# Copyright 2019-2022 CNRS-AIST JRL

from bibmanagement.fields import Month
import unittest

class TestMonth(unittest.TestCase):
    def test(self):
        m = Month.Month.fromString('March 23rd')
        
        self.assertEqual(str(m.format('%mm%')), '03')

if __name__ == '__main__':
    unittest.main()