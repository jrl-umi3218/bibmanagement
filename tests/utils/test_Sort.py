from bibmanagement.utils import Sort
import unittest

class TestSort(unittest.TestCase):
    def test_MixComp(self):
        cmp = Sort.MixComp(['>', '<', '<'])
        self.assertFalse(cmp((1,2,3), (2,2,3)))
        self.assertTrue(cmp((1,2,3), (0,2,3)))
        self.assertTrue(cmp((1,2,3), (1,3,3)))
        self.assertFalse(cmp((1,2,3), (1,1,3))) 
        self.assertTrue(cmp((1,2,3), (1,2,4)))
        self.assertFalse(cmp((1,2,3), (1,2,2)))
        self.assertFalse(cmp((1,2,3), (1,2,3)))
        
if __name__ == '__main__':
    unittest.main()