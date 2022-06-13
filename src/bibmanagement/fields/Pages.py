# Copyright 2019-2022 CNRS-AIST JRL

from bibmanagement.fields.Field import Field
from bibmanagement.fields import FormatExpr
from bibmanagement.utils.FormattedString import Single
from bibmanagement import log

logger = log.getBibLogger(__name__)

class Pages(Field):

    _defaultFormatExpr = '%p% %f%[-]%l%'

    """Page numbers, separated either by commas or double-hyphens."""
    def __init__(self, first, last=None):
        self._first = first
        if last:
            if last<first:
                raise ValueError("Last page number can't be smaller than first page number.")
            else:
                self._last = last
        else:
            self._last = None

    @classmethod
    def _fromString(cls, str, e):
        if ',' in str:
            raise NotImplementedError()
        try:
            pages = [int(p) for p in str.split('-') if len(p.strip()) > 0]
        except:
            logger.warning(e, 'unexpected_page_format', str)
            return cls(str)
        n = len(pages)
        if n > 2:
            #raise ValueError("Too many page numbers.")
            logger.warning(e, 'unexpected_page_format', str)
            return cls(str)
        if n < 1:
            raise ValueError("No page number found")
        if n == 1:
            return cls(pages[0])
        else:
            return cls(pages[0], pages[1])

    def isRange(self):
        return self._last != None

    def _writePage(self, formatString):
        if self.isRange():
            if formatString == 'p':
                return 'pp.'
            if formatString == 'P':
                return 'PP.'
            if formatString == 'page':
                return 'pages'
            if formatString == 'Page':
                return 'Pages'
            if formatString == 'pages':
                return 'pages'
            if formatString == 'Pages':
                return 'Pages'
        else:
            if formatString == 'p':
                return 'p.'
            if formatString == 'P':
                return 'P.'
            if formatString == 'page':
                return 'page'
            if formatString == 'Page':
                return 'Page'
            if formatString == 'pages':
                return 'page'
            if formatString == 'Pages':
                return 'Page'

        raise ValueError('Incorrect format string')

    def _format(self, formatExpr, style):
        """
        Replace the placeholders in formatExpr with the relevant data.
        Placeholders can be:
         - %p%, %P%, %page%, %Page%, %pages%, %Pages% to specify how the word 'page' will be displayed 
           (this also depends on the fact that we have a single page or a page range)
         - %f%, %l% to specify the first and last page number
        %pl% will be replaced by '' in case this is not a page range.
        """

        placeholders = ['p', 'P', 'page', 'Page', 'pages', 'Pages', 'f', 'l']
        f = FormatExpr.FormatExpr(placeholders, formatExpr)
        l = f.placeholderList()
        replacements = []

        for e in l:
            if 'p' in e or 'P' in e:
                replacements.append(self._writePage(e))
            if 'f' in e:
                replacements.append(str(self._first))
            if 'l' in e:
                if self._last:
                    replacements.append(str(self._last))
                else:
                    replacements.append('')

        return Single('pages', f.reduce(replacements), style)
