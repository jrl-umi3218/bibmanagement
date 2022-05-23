from bibmanagement.utils.FormattedString import Style

class Field:
    """Base abstract class for all fields"""

    #Default format expression. Will be overwritten by derived class
    _defaultFormatExpr = ''

    def format(self, formatExpr=None, style=None):
        fe = formatExpr if formatExpr else self._defaultFormatExpr
        r = self._format(fe, style)
        if r.style:
            r.style = Style.fromString(r.style)
        return r

    def execute(self,cmd):
        s = cmd.split('(')
        if len(s) == 1: # there was no open parenthesis: this should be a field
            return getattr(self,cmd,'')
        else:
            if s[1] and s[1][-1] == ')':
                f = getattr(self,s[0],None)
                if callable(f):
                    if len(s[1])==1:
                        return f()
                    else:
                        arg = [a.strip() for a in s[1][0:-1].split(',')]
                        return f(*arg)
                else:
                    raise ValueError(s[0] + ' is not a method for this field.')
            else:
                raise ValueError('('+s[1] + ' is not a well-formed argument.')
                
    def __str__(self):
        return str(self.format())

    def _format(self, formatExpr, style):
        raise NotImplementedError()

    @classmethod
    def fromString(cls, str, e = None):
        f = cls._fromString(str, e)
        f.entry = e
        return f
        
    @classmethod
    def _fromString(cls, str, e = None):
        raise NotImplementedError()


# Standard fields
#address
#annote
#author
#booktitle
#chapter
#crossref
#doi
#edition
#editor
#howpublished
#institution
#journal
#key
#month
#note
#number
#organization
#pages
#publisher
#school
#series
#title
#type
#volume
#year

