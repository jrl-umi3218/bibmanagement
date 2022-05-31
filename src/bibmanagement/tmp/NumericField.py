from bibmanagement.Fields.Field import Field
from bibmanagement.utils.FormattedString import Single
from bibmanagement import log

logger = log.getBibLogger(__name__)

import warnings

class NumericField(Field):

    _defaultFormatExpr = '%num%'

    @staticmethod
    def _makeOrdinal(n, e=None):
        """ Return a string representing the ordinal number corresponding to n"""
        
        if isinstance(n, str):
            logger.warning(e, 'numeric_value_expected', n)
            return n

        if not isinstance(n, int):
            logger.warning(e, 'non_integer', str(n), '_makeOrdinal')

        l = n%10
        ll = n%100
        if l==1 and ll!=11:
            return str(n)+'st'
        if l==2 and ll!=12:
            return str(n)+'nd'
        if l==3 and ll!=13:
            return str(n)+'rd'
        return str(n)+'th'

    @staticmethod
    def _makeAlphaOrdinal(n, e=None):
        """Return a string representing the ordinal number written with alphabetical characters"""
        if isinstance(n, str):
            logger.warning(e, 'numeric_value_expected', n)
            return n
        
        if not isinstance(n, int):
            logger.warning(e, 'non_integer', str(n), '_makeAlphaOrdinal')

        if n < 1:
            raise ValueError("n needs to be at least one")
        if n >= 10000:
            raise NotImplementedError()

        firstCard = ['', 'first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 
                     'tenth', 'eleventh', 'twelfth', 'thirteenth', 'fourteenth', 'fifteenth', 'seventeenth', 'eighteenth', 'nineteenth']
        unit = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
        tens = ['', 'ten', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']

        if n<20:
            return firstCard[n]
        
        u = n%10
        t = (int(n/10))%10
        h = (int(n/100))%10
        l = int(n/1000)

        s = ''
        if l>0:
            if h==0 and t==0 and u==0:
                s = unit[l] + ' thousandth'
            else:
                s = unit[l] + ' thousand '
        if h > 0:
            if t==0 and u==0:
                s += unit[h] + ' hundredth'
            else:
                s += unit[h] + ' hundred '
        if t>0:
            if u==0:
                s += tens[t][0:-1] + 'ieth'
            else:
                s += tens[t] + '-'
        if u>0:
            s += firstCard[u]

        return s



    def __init__(self, val):
        self._val = val

    @classmethod
    def _fromString(cls, s, e):
        try:
            v = int(s)
        except:
            logger.warning(e, 'numeric_value_expected', s)
            v = s
        return cls(v)

    def _format(self, formatExpr, style):
        n = formatExpr.count('%')
        if n != 2:
            raise ValueError('Format expr must include exactly one placeholder (enclosed by %)')

        s = formatExpr.replace('%num%', str(self._val))\
                      .replace('%ord%', NumericField._makeOrdinal(self._val, self.entry))\
                      .replace('%th%', NumericField._makeOrdinal(self._val, self.entry))

        return Single(self.__class__.__name__.lower(), s, style)
