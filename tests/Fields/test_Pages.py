# Copyright 2019-2022 CNRS-AIST JRL

from bibmanagement.fields import Pages
import unittest

class TestPages(unittest.TestCase):
    def test_1(self):
        p1 = Pages.Pages.fromString('10--15')
        p2 = Pages.Pages(3)
        
        self.assertEqual(str(p1.format('%page% %f%[--]%l%')), 'pages 10--15')
        self.assertEqual(str(p2.format('%page% %f%[--]%l%')), 'page 3')
        self.assertEqual(str(p1.format('%p% %f%[ - ]%l%')), 'pp. 10 - 15')
        self.assertEqual(str(p2.format('%p% %f%[-]%l%')), 'p. 3')
    
if __name__ == "__main__":
    unittest.main()