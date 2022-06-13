# Copyright 2019-2022 CNRS-AIST JRL

from bibmanagement.utils import FormattedString as fs
import copy

class Filter:
    '''Change the style of a (formatted) string based on its type and its content'''

    def __init__(self, type='any', contains=None, equals=None, applyToAll=False, bold=None, italic=None, underline=None, strikethrough=None, font=None, fontSize=None):
        if (equals and contains) or (not equals and not contains):
            raise ValueError('Please set a value for contains or equals, and not both.')
        self._type = type
        self._contains = contains
        self._equals = equals
        self._applyToAll = applyToAll
        self._bold = bold
        self._italic = italic
        self._underline = underline
        self._strikethrough = strikethrough
        self._font = font
        self._fontSize = fontSize

    def __call__(self, s):
        if isinstance(s, str):
            if self._type=='any':
                return self._process(s, None)
            else:
                return fs.Single('string',s)
        elif isinstance(s, fs.Single):
            if s.type==self._type or self._type=='any':
                return self._process(s.string, s.style, s.type)
            else:
                return s
        elif isinstance(s, fs.Multiple):
            out = fs.Single.Empty()
            for single in s.singles:
                out = out + self(single)
            return out
        else:
            raise TypeError('Can only process string, FormattedString.Single and FormattedString.Multiple, not ' + s.__class__)


    def _process(self, s, currStyle, type='string'):
        b, sub, spl = self._check(s)
        if b:
            if currStyle:
                newStyle = copy.copy(currStyle)
                newStyle.set(self._bold, self._italic, self._underline, self._strikethrough, self._font, self._fontSize)
            else:
                newStyle = fs.Style(self._bold, self._italic, self._underline, self._strikethrough, self._font, self._fontSize)

            if self._applyToAll:
                return fs.Single(type, s, newStyle)
            else:
                sspl = [fs.Single.Empty() if e=='' else fs.Single(type, e, currStyle) for e in spl]
                out = sspl[0]
                for i in range(1,len(spl)):
                    out = out + fs.Single(type, sub, newStyle) + sspl[i]
                return out
        else:
            return fs.Single(type, s, currStyle)

    def _check(self, s):
        '''
        Check if s contains or is equal to the specified string, depending on _contains and _equals.
        Returns as well the specified string and the parts around it.
        '''
        if self._contains:
            spl = s.split(self._contains)
            return len(spl)>1, self._contains, spl
        if self._equals:
            return s == self._equals, self._equals,  ['','']
