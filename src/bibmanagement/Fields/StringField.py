from bibmanagement.Fields.Field import Field
from bibmanagement.utils.FormattedString import Single

class StringField(Field):

    _defaultFormatExpr = '%s%'

    @staticmethod
    def _capitalize(str, all=False):
        """Capitalize the first letter of a str, or of each word of str if all is true"""
        if all:
            words = str.split()
            if len(words) > 1:
                sep = ' '
                return sep.join([StringField._capitalize(w) for w in words])

        if len(str)>1:
            return str[0].upper() + str[1:len(str)].lower()
        else:
            return str.upper()


    def __init__(self, str):
        self._val = str

    @classmethod
    def _fromString(cls, str, e):
        return cls(str)

    def _format(self, formatExpr, style):
        """
		Format option:
		 - %s%, %S%: same value as inputed
		 - %ss%: all lower case
		 - %SS%: all upper case
		 - %Ss%: first letter upper case, rest lower case
		 - %SsSs%: all words are capitalized
		"""

        n = formatExpr.count('%')
        if n != 2:
            raise ValueError('Format expr must include exactly one placeholder (enclosed by %)')

        s = formatExpr.replace('%s%', self._val)\
	                   .replace('%S%', self._val)\
                       .replace('%ss%', self._val.lower())\
                       .replace('%SS%', self._val.upper())\
                       .replace('%Ss%', StringField._capitalize(self._val))\
                       .replace('%SsSs%', StringField._capitalize(self._val, True))

        return Single(self.__class__.__name__.lower(),s, style)