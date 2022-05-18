from bibmanagement.Fields import FormatExpr
import unittest

class TestFormatExpr(unittest.TestCase):
    def test_1(self):
        ph = ['field1', 'field2', 'field3', 'field4', 'field5']

        def test(expr,replacements,expected):
            format = FormatExpr.FormatExpr(ph, expr)
            s = format.reduce(replacements)
            self.assertEqual(s, expected)

        test('%field1% + %field2% = %field3%', ['1','2','3'], '1 + 2 = 3')
        test('%field2%[/]%field3%', ['1','2'], '1/2')
        test('%field2%[/]%field3%', ['1','#'], '1')
        test('%field2%[/]%field3%', ['#','2'], '2')

        test('%field1%[, %field2%][, ]%field3%', ['1', '2', '3'], '1, 2, 3')
        test('%field1%[, %field2%][, ]%field3%', ['1', '2', '#'], '1, 2')
        test('%field1%[, %field2%][, ]%field3%', ['1', '#', '3'], '1, 3')
        test('%field1%[, %field2%][, ]%field3%', ['#', '2', '3'], ', 2, 3')
        test('%field1%[, %field2%][, ]%field3%', ['1', '#', '#'], '1')
        test('%field1%[, %field2%][, ]%field3%', ['#', '2', '#'], ', 2')
        test('%field1%[, %field2%][, ]%field3%', ['#', '#', '3'], '3')
        test('%field1%[, %field2%][, ]%field3%', ['#', '#', '#'], '')

        test('%field1%[, ]%field2%[, ]%field3%', ['1', '2', '3'], '1, 2, 3')
        test('%field1%[, ]%field2%[, ]%field3%', ['1', '2', '#'], '1, 2')
        test('%field1%[, ]%field2%[, ]%field3%', ['1', '#', '3'], '1, 3')
        test('%field1%[, ]%field2%[, ]%field3%', ['#', '2', '3'], '2, 3')
        test('%field1%[, ]%field2%[, ]%field3%', ['1', '#', '#'], '1')
        test('%field1%[, ]%field2%[, ]%field3%', ['#', '2', '#'], '2')
        test('%field1%[, ]%field2%[, ]%field3%', ['#', '#', '3'], '3')
        test('%field1%[, ]%field2%[, ]%field3%', ['#', '#', '#'], '')

        test(r'[\[%field1%\]]', ['1'], '[1]')
        test(r'\%%field1%', ['1'], '%1')
    
    def test_unusedChar(self):
        s = 'testing'
        forbidden = '#@-='
        c = FormatExpr.unusedChar(s, forbidden)
        self.assertFalse(c in s)
        self.assertFalse(c in forbidden)
        
        c2 = FormatExpr.unusedChar(s, forbidden, 3)
        self.assertFalse(c2[0] in s)
        self.assertFalse(c2[0] in forbidden)
        self.assertFalse(c2[1] in s)
        self.assertFalse(c2[1] in forbidden)
        self.assertFalse(c2[2] in s)
        self.assertFalse(c2[2] in forbidden)
        
        with self.assertRaises(ValueError):
            FormatExpr.unusedChar('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', '#@!%&-_=,0123456789')
        
    def test_error(self):
        with self.assertRaises(ValueError):
            FormatExpr.FormatExpr(['%wrong'], '')
            
        fe = FormatExpr.FormatExpr(['test'], 'expr')
        with self.assertRaises(ValueError):
            fe.reduce(['two', 'too', 'many'])
            
        with self.assertRaises(ValueError):
            FormatExpr.FormatExpr(['test'], '[[nested]]')
            
        with self.assertRaises(ValueError):
            FormatExpr.FormatExpr(['test'], '%expr1-%expr2%')
            
        with self.assertWarns(UserWarning):
            FormatExpr.FormatExpr(['test'], '%expr%')
        
        with self.assertRaises(ValueError):
            FormatExpr.FormatExpr([], '[bracket]')
            
        with self.assertRaises(ValueError):
            FormatExpr.FormatExpr([], 'test[bracket]')
            
        with self.assertRaises(ValueError):
            FormatExpr.FormatExpr(['ph1', 'ph2'], '%ph1%constant[sep]%ph2%')
        
        with self.assertRaises(ValueError):
            FormatExpr.FormatExpr(['ph1', 'ph2'], '%ph1%[sep]constant%ph2%')
        
    
if __name__ == '__main__':
    unittest.main()