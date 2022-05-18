from bibmanagement.Fields import Date
import unittest

#helper to test nested functions, from https://stackoverflow.com/a/40512422
import types

def freeVar(val):
  def nested():
    return val
  return nested.__closure__[0]

def nested(outer, innerName, **freeVars):
  if isinstance(outer, (types.FunctionType, types.MethodType)):
    outer = outer.__code__
  for const in outer.co_consts:
    if isinstance(const, types.CodeType) and const.co_name == innerName:
      return types.FunctionType(const, globals(), None, None, tuple(
          freeVar(freeVars[name]) for name in const.co_freevars))


class TestDate(unittest.TestCase):
    def test_simple(self):
        d = Date.Date('March 3rd, 2020')
        self.assertFalse(d.hasDayRange())
        self.assertFalse(d.hasMonthRange())
        self.assertFalse(d.hasYearRange())
        self.assertFalse(d.isRange())
        self.assertEqual(d.day(), 3)
        self.assertEqual(d.month(), 'March')
        self.assertEqual(d.year(), 2020)
        
        d = Date.Date('March 3rd, 2020 -- April 6th, 2021')
        self.assertTrue(d.hasDayRange())
        self.assertTrue(d.hasMonthRange())
        self.assertTrue(d.hasYearRange())
        self.assertTrue(d.isRange())
        self.assertEqual(d.day(), [3,6])
        self.assertEqual(d.month(), ['March', 'April'])
        self.assertEqual(d.year(), [2020,2021])
        
        d1 = Date.Date('March 3rd')
        self.assertFalse(d1.year())
        
        d2 = Date.Date('2022')
        self.assertFalse(d2.day())
        self.assertFalse(d2.month())

    def test_parse(self):
        import random
        chars = [' ', ' ', ' ', 'd', 'm', 'y']
        accepted = Date._acceptedFormat()
        def generatePattern():
            """ Generate a random pattern """
            useRange = random.random()>=0.5
            s1 = ''
            s = ''
            for i in range(0,4):
                s1 = s1 + random.choice(chars)
            if useRange:
                s2 = ''
                for i in range(0,4):
                    s2 = s2 + random.choice(chars)
                s = (s1+'-'+s2).replace(' ', '')
            else:
                s = s1.replace(' ', '')
            return (s, s in accepted)

        days1 = {'1':True, '15': True, '07': True, '0': False}
        days2=  {'19': True, '21': True, '27': True, '123':False}
        months1 = {'January':True, 'february':True, 'mar': True, 'Apr': True, 'Decemberq': False, 'other': False}
        months2 = {'May': True, 'Jun.':True, 'jul.':True, 'aug': True, 'Sept':False, 'Octobre':False,  'november':True}
        years1 = {'1687':True, '889': False, '1902,': True, '1982': True}
        years2 = {'2014': True, '3201': False, '2899': True, '2006,': True}
        sep = {'-': True, '-': True, '-': True, '--' : True, '---': False, '&': False}
        map1 = {'d':days1, 'm':months1, 'y':years1, '-':sep}
        map2 = {'d':days2, 'm':months2, 'y':years2, '-':sep}

        for i in range(0,10000):
            p, shouldWork = generatePattern()
            string = ''
            after = False  #before or after dash
            for c in p:
                if c == '-':
                    after = True
                if after:
                    s,b = random.choice([*map2[c].items()])
                else:
                    s,b = random.choice([*map1[c].items()])
                string = string + s + ' '
                shouldWork = shouldWork and b

            try:
                d = Date.Date(string)
                self.assertTrue(shouldWork, msg='Fails to catch error for \n  ' + string)
            except:
                self.assertFalse(shouldWork, msg='Unexpected failure\n  ' + string)
                
        with self.assertRaises(ValueError):
            d = Date.Date('February 30th')
        with self.assertRaises(ValueError):
            d = Date.Date('March 3rd - March 1st')

    def test_format(self):
        d0 = Date.Date('March 3rd')
        d1 = Date.Date('March 3rd, 2020')
        d2 = Date.Date('March 3rd, 2020 -- April 6th, 2021')
        d3 = Date.Date('March 3rd, 2020 -- April 6th, 2020')
        d4 = Date.Date('March 3-5')
        d5 = Date.Date('2014')
        
        self.assertEqual(d0.format('%y%'), '')
        self.assertEqual(d0.format('%Month%'), 'March')
        self.assertEqual(d0.format('%month%'), 'march')
        self.assertEqual(d0.format('%MONTH%'), 'MARCH')
        self.assertEqual(d1.format('%Mon%'), 'Mar')
        self.assertEqual(d1.format('%mon%'), 'mar')
        self.assertEqual(d1.format('%MON%'), 'MAR')
        self.assertEqual(d1.format('%mon.%'), 'mar.')
        self.assertEqual(d1.format('%MON.%'), 'MAR.')
        self.assertEqual(d1.format('%m%'), '3')
        self.assertEqual(d1.format('%M%'), '3')
        self.assertEqual(d1.format('%dayth%'), '3rd')
        
        self.assertEqual(d1.format('%Day%'), '3')
        self.assertEqual(d1.format('%dd1%'), '03')
        self.assertEqual(d1.format('%d2%'), '')
        self.assertEqual(d1.format('%mm%'), '03')
        self.assertEqual(d1.format('%Mon.1%'), 'Mar.')
        self.assertEqual(d1.format('%MONTH2%'), '')
        self.assertEqual(d1.format('%yy%'), '20')
        self.assertEqual(d1.format('%yyyy1%'), '2020')
        self.assertEqual(d1.format('%y2%'), '')
        
        self.assertEqual(d2.format('%dd%/%mm% - %dd%/%mm%'), '03/03 - 06/04')
        self.assertEqual(d2.format('%mm1%'), '03')
        self.assertEqual(d2.format('%mm2%'), '04')
        self.assertEqual(d2.format('%Year% - %YY%'), '2020 - 21')
        self.assertEqual(d2.format('%Year2% - %YY1%'), '2021 - 20')
        self.assertEqual(d2.format('%dd2% - %dd1%'), '06 - 03')
        
        self.assertEqual(d3.format('%Year% - %YY%'), '2020 -')
        
        self.assertEqual(d4.format('%MM% - %mm%'), '03 -')
        self.assertEqual(d5.format('%mm%'), '')
        self.assertEqual(d5.format('%dd%'), '')
        
        #additional coverage
        nestedFormatYear = nested(Date.Date._formatYear, 'format', self=d1)
        nestedFormatDay = nested(Date.Date._formatDay, 'format', self=d1)
        with self.assertRaises(ValueError):
            nestedFormatYear(0,'yer', False)
        self.assertEqual(d2._formatYear('y', 3), '')
        self.assertEqual(d2._formatMonth('m', 3), '')
        self.assertEqual(d2._formatDay('d', 3), '')
        with self.assertRaises(ValueError):
            d1._formatYear('yer')
        with self.assertRaises(ValueError):
            d2._formatYear('yer')
        with self.assertRaises(ValueError):
            d2._formatMonth('monh')
        self.assertEqual(nestedFormatDay(0, 'dd', True), '')
        with self.assertRaises(ValueError):
            d2._formatDay('dayt')

    def test_ordinal(self):
        input = [1, 2, 3, 4, 5, 6, 7, 8, 9,  10 , 11, 12, 13, 14, 20, 21, 22, 23, 24]
        ans = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th', '13th', '14th', '20th', '21st', '22nd', '23rd', '24th']
        for i,a in zip(input, ans):
            self.assertEqual(a, Date.Date._makeOrdinal(i), msg='Unexpected output for ' + str(i))

if __name__ == '__main__':
    unittest.main()
