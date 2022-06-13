# Copyright 2019-2022 CNRS-AIST JRL

from bibmanagement.fields import Authors
import unittest

class TestAuthors(unittest.TestCase):
    def test_single(self):
        s = "Herzog, Alexander"
        a = Authors.Authors.fromString(s)
        self.assertEqual(str(a.format('{%first% %last%}{, }{ and }{}')), 'alexander herzog')
    
    def test_multiple(self):
        s = "Herzog, Alexander and Rotella, Nicholas and Mason, Sean and Grimminger, Felix and Schaal, Stefan and Righetti, Ludovic"
        a = Authors.Authors.fromString(s)
    
        self.assertEqual(str(a.format('{%F% %Last%}{, }{ and }{}')), 'A. Herzog, N. Rotella, S. Mason, F. Grimminger, S. Schaal and L. Righetti')
        self.assertEqual(str(a.format('{%F% %Last%}{, }{ and }{2}')), 'A. Herzog, N. Rotella et al.')
        self.assertEqual(str(a.format('{%F% %Last%}{, }{ and }{5}')), 'A. Herzog, N. Rotella, S. Mason, F. Grimminger, S. Schaal and L. Righetti')
        self.assertEqual(str(a.format('{%F% %Last%}{, }{ and }{5!}')), 'A. Herzog, N. Rotella, S. Mason, F. Grimminger, S. Schaal et al.')
        
        # Test indexation
        self.assertEqual(str(a[2].format('%F% %L%')), 'S. M.')
        
        with self.assertRaises(ValueError):
            a.format('{%F% %Last%}{, }{}')
        
    def test_coverage(self):
        with self.assertRaises(ValueError):
            Authors.Authors._extractBracedParts('%F%')
        with self.assertRaises(ValueError):
            Authors.Authors._extractBracedParts('{{%F%}{%L%}')
    
if __name__ == '__main__':
    unittest.main()