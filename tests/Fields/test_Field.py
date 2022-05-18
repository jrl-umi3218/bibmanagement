from bibmanagement.Fields import Field
from bibmanagement.Fields import NumericField
from bibmanagement.Fields import Pages
import unittest

class Test(unittest.TestCase):
    def test(self):
        nf = NumericField.NumericField.fromString('21')
        
        fm = nf.format('%num%', 'i,12')
        self.assertEqual(str(fm.string), '21')
        self.assertFalse(fm.style.bold)
        self.assertTrue(fm.style.italic)
        self.assertFalse(fm.style.underline)
        self.assertFalse(fm.style.strikethrough)
        self.assertEqual(fm.style.fontSize, 12)
        self.assertEqual(fm.style.font, 'Calibri')
        
    def test_execute(self):
        nf = NumericField.NumericField.fromString('21')
        p = Pages.Pages(3,5)
        
        self.assertEqual(nf.execute('_val'), 21)
        self.assertEqual(str(nf.execute('_format(%ord%, \'\')')), '21st')
        self.assertTrue(p.execute('isRange()'))
        
        with self.assertRaises(ValueError):
            nf.execute('wrong()')
        with self.assertRaises(ValueError):
            p.execute('isRange(')
            
    def test_coverage(self):
        nf = NumericField.NumericField.fromString('21')
        self.assertEqual(str(nf), '21')
        
        with self.assertRaises(NotImplementedError):
            Field.Field()._format('%ord%', '')
        with self.assertRaises(NotImplementedError):
            Field.Field.fromString('')
    

if __name__ == '__main__':
    unittest.main()