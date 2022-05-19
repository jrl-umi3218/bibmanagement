from bibmanagement.Fields.Field import Field
from bibmanagement.Fields.Date import Date
from bibmanagement.utils.FormattedString import Single

class Month(Field):
    """The month of publication (or, if unpublished, the month of creation)"""

    _defaultFormatExpr = '%Month1% %day1%[-][%Month2% ]%day2%'
    
    def __init__(self, date):
        assert isinstance(date, Date)
        assert not date.year()

        self._date = date

    @classmethod
    def _fromString(cls, str):
        date = Date(str)
        return cls(date)
        
    def _format(self, formatExpr, style):
        return Single('month', self._date.format(formatExpr), style)
