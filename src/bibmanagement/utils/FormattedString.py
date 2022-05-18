class Style:
    '''A class specifying the style of some text.'''
    _defaultBold = False
    _defaultItalic = False
    _defaultUnderline = False
    _defaultStrikethrough = False
    _defaultFont = 'Calibri'
    _defaultFontSize = 11

    @staticmethod
    def setDefault(default):
        '''
        Set the default set values for a style. 
        These values will be used when constructing a new instance of the class when the corresponding fields are not specified.'''
        _defaultBold = default._bold
        _defaultItalic = default._italic
        _defaultUnderline = default._underline
        _defaultStrikethrough = default._strikethrough
        _defaultFont = default._font
        _defaultFontSize = default._fontSize

    def __init__(self, bold=_defaultBold, italic=_defaultItalic, underline=_defaultUnderline, strikethrough=_defaultStrikethrough, font=_defaultFont, fontSize=_defaultFontSize):
        self.bold = bold if bold else Style._defaultBold
        self.italic = italic if italic else Style._defaultItalic
        self.underline = underline if underline else Style._defaultUnderline
        self.strikethrough = strikethrough if strikethrough else Style._defaultStrikethrough
        self.font = font if font else Style._defaultFont
        self.fontSize = fontSize if fontSize else Style._defaultFontSize

    def set(self, bold=None, italic=None, underline=None, strikethrough=None, font=None, fontSize=None):
        if bold!=None:
            self.bold = bold
        if italic!=None:
            self.italic = italic
        if underline!=None:
            self.underline = underline
        if strikethrough!=None:
            self.strikethrough = strikethrough
        if font!=None:
            self.font = font
        if fontSize!=None:
            self.fontSize = fontSize



    @classmethod
    def fromString(cls, s):
        '''
        Parse a comma-separated list where the elements can be:
         - a font name,
         - a font size,
         - b or bold,
         - i or italic,
         - u or underline,
         - s or strike
        '''
        fs = cls()

        l = s.split(',')
        for e in l:
            es = e.strip()
            if es=='b' or es=='bold':
                fs.bold = True
            elif es=='i' or es=='italic':
                fs.italic = True
            elif es=='u' or es=='underline':
                fs.underline = True
            elif es=='s' or es=='strike':
                fs.strikethrough = True
            elif es.isdigit():
                fs.fontSize = int(es)
            else:
                fs.font = es
        return fs


class Single:
    '''
    A string, with a single style and a type.
    The type is used to specify what kind of value the string represents and can be leveraged in filtering.
    The style specify how the string should be displayed upon export (however exporter may ignore the style).

    A Single is considered empty if its type is 'none' and its string is empty
    '''
    def __init__(self, type, string, style=None):
        self.type = type
        self.string = string
        self.style = style
        self._empty = type == 'none' and string == ''

    def __add__(self, other):
        if self._empty:
            return other
        if isinstance(other, Single):
            if other.isEmpty():
                return self
            else:
                return Multiple([self, other])
        elif isinstance(other, Multiple):
            return Multiple([self] + other.singles)
        elif isinstance(other, str):
            if other=='':
                return self
            else:
                return self + Single('string', other)
        else:
            raise TypeError("Cannot add object of type " + other.__class__ + " to a FormattedString.Single")

    def __radd__(self, other):
        if isinstance(other, str):
            if other=='':
                return self
            else:
                return Single('string', other) + self
        else:
            raise TypeError("Cannot add object of type " + other.__class__ + " to a FormattedString.Single")

    def __str__(self):
        return self.string

    def isEmpty(self):
        return self._empty

    @staticmethod
    def Empty():
        '''Create an empty Single'''
        return Single('none', '')


class Multiple:
    '''A list of Single'''
    def __init__(self, singles):
        self.singles = singles

    def __add__(self, other):
        if isinstance(other, Single):
            if other.isEmpty():
                return self
            else:
                return Multiple(self.singles + [other])
        elif isinstance(other, Multiple):
            return Multiple(self.singles + other.singles)
        elif isinstance(other, str):
            if other=='':
                return self
            else:
                return self + Single('string', other)
        else:
            raise TypeError("Cannot add object of type " + type(other) + " to a FormattedString.Single")

    def __radd__(self, other):
        if isinstance(other, str):
            if other=='':
                return self
            else:
                return Single('string', other) + self
        else:
            raise TypeError("Cannot add object of type " + other.__class__ + " to a FormattedString.Single")

    def __str__(self):
        s = ''
        for e in self.singles:
            s += str(e)
        return s