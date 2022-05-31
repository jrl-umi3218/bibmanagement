from bibmanagement.fields.Field import Field
from bibmanagement.fields.Date import Date
from bibmanagement.utils.FormattedString import Single

class Month(Field):
    """The month of publication (or, if unpublished, the month of creation)"""

    _defaultFormatExpr = '%Month1% %day1%[-][%Month2% ]%day2%'
    
    def __init__(self, date):
        assert isinstance(date, Date)
        assert not date.year()

        self._date = date

    @classmethod
    def _fromString(cls, str, e):
        date = Date(str)
        return cls(date)
        
    def _format(self, formatExpr, style):
        return Single('month', self._date.format(formatExpr), style)
