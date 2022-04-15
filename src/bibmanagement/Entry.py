from Fields.Authors import *
from Fields.BasicFields import *
from Fields.NonStandardFields import *
from Fields.Month import *
from Fields.Pages import *
from Fields.Journal import Journal
from Fields.Booktitle import Booktitle
from utils.FormattedString import Single
import FormatExpr.Formatter as Formatter
from bibtexparser.latexenc import string_to_latex
import sys

class BaseEntry:
    _formatter = Formatter.Formatter()

    #: List containing the names of the tags which are required for the BibTeX entry type.
    #: *It will be overwritten by the subclass definition.*
    _requiredTags = []

    #: List containing the names of the tags which are defined as optional by BibTeX. This list
    #: only serves in very few cases. Otherwise it is mainly here for information and detecting
    #: additional tags.
    #: *It will be overwritten by the subclass definition.*
    _optionalTags = []

    __fieldMap = {'address': 'Address',
                  'annote': 'Annote',
                  'author': 'Authors',
                  'booktitle': 'Booktitle',
                  'chapter': 'Chapter',
                  'crossref': 'Crossref',
                  'doi': 'Doi',
                  'edition': 'Edition',
                  'editor': 'Editor',
                  'howpublished': 'HowPublished',
                  'institution': 'Institution', 
                  'journal': 'Journal',
                  'key': 'Key',
                  'month': 'Month',
                  'note': 'Note',
                  'number': 'Number',
                  'organization': 'Organization',
                  'pages': 'Pages',
                  'publisher': 'Publisher',
                  'school': 'School',
                  'series': 'Series',
                  'title': 'Title',
                  'type': 'Type',
                  'volume': 'Volume',
                  'year': 'Year',
                  'abstract' : 'Abstract',
                  'acmid' : 'Acmid',
                  'hal_id' : 'Hal_id',
                  'hal_version' : 'Hal_version',
                  'keywords' : 'Keywords',
                  'pdf' : 'Pdf',
                  'url': 'Url',
                  'lab': 'Lab',
                  'isbn': 'Isbn',
                  'todo': 'Todo'}

    def __init__(self, data):
        self._raw = {}
        self._fields = {}
        self._raw['ID'] = data.get('ID',None)
        self._raw['ENTRYTYPE'] = data.get('ENTRYTYPE',None)
        self.id = self._raw['ID']
        self._fields['ID'] = self.id
        for tag,val in data.items():
            if tag != 'ID' and tag != 'ENTRYTYPE':
                t = tag.lower()
                self._raw[t] = val
                if t in BaseEntry.__fieldMap:
                    setattr(self, t, eval(BaseEntry.__fieldMap[t]).fromString(val))
                    self._fields[t] = getattr(self, t)
                else:
                    print("Unrecognized field name " + tag + " in entry " + self._raw['ID'], file=sys.stderr)

    def __iter__(self):
        return iter(self._fields)

    def raw(self):
        return self._raw

    def keys(self):
        """
        Returns a list of tag names defined for the entry object.

        :return: list of tag names
        :rtype: list
        """
        return self._fields.keys()

    def values(self):
        """
        Returns a list of tags contents defined for the entry object.

        :return: list of tags contents
        :rtype: list
        """
        return self._fields.values()

    def items(self):
        """
        Returns a list of sets containing tag name/value.

        :return: list of sets tag name/value
        :rtype: list
        """
        return self._fields.items()

    def __setitem__(self, key, value):
        """
        Method to (re)set a tag.

        :param key: tag name
        :type key: str
        :param value: tag contents
        """
        if key in BaseEntry.__fieldMap:
            if isinstance(value, str):
                setattr(self, key, eval(BaseEntry.__fieldMap[key]).fromString(value))
                self._raw[key] = value
            else:
                if isinstance(value, eval(BaseEntry.__fieldMap[key])):
                    setattr(self, key, value)
                    self._raw[key] = str(value)
                else:
                    raise TypeError('Attempt to assign an incorrect type')
            self._fields[key] = getattr(self, key)
        else:
            print("Unrecognized field name " + key + " in entry " + self.id, file=sys.stderr)

    def get(self, key, default=None):
        """
        Return the contents for a tag name if tag is defined for the Entry, else default.

        :param name: tag name
        :type name: str
        :param default: default return if tag is not defined
        :return: tag contents
        """
        if key[0] == '\\':
            return self._raw.get(key[1:], default)
        else:
            s = key.split('.')
            if len(s)==1:
                return self._fields.get(key, default)
            else:
                f = self._fields.get(s[0], default)
                return f.execute(s[1]) if f else '' 


    def __getitem__(self, key):
        """
        Return the contents for a tag name if tag is defined for the Entry, else default.
        If the tag starts with a backslash, get the raw string rather than the processed field

        :param key: tag name
        :type key: str
        :return: tag contents
        """
        if key[0] == '\\':
            return self._raw[key[1:]]
        else:
            s = key.split('.')
            if len(s)==1:
                return self._fields[key]
            else:
                f = self._fields[s[0]]
                return f.execute(s[1])


    def del_tag(self, name):
        """
        Method to delete a tag.

        :param name: tag name
        :type name: str
        :raises KeyError: if tag is not defined in entry
        """
        del self[name]

    def __delitem__(self, key):
        """
        Method to delete a tag.

        :param key: tag name
        :type key: str
        :raises KeyError: if tag is not defined in entry
        """
        if key not in self._fields:
            msg = 'Tag not found in Entry!'
            raise KeyError(msg)
        del self._raw[key]
        del self._fields[key]
        delattr(self, key)

    def __contains__(self, key):
        return key in self._fields

    def format(self, formatExpr):
        r = BaseEntry._formatter.run(self, formatExpr)
        if r:
            return r
        else:
            return Single.Empty()

    def additionnalTags(self):
        pass
        
    def integrateCrossref(self, other):
        for k in other.keys():
            if k not in self and k != 'ID':
                self[k] = other[k]
                
    def toString(self, ignoreField=None):
        if ignoreField:
            ignoreField += ['ID', 'ENTRYTYPE']
        else:
            ignoreField = ['ID', 'ENTRYTYPE']
        sizeMax = max([len(k) for k in self._raw.keys() if k not in ignoreField])
        s = "@{}{{{},\n".format(self.__class__.__name__, self.id)
        includedTags = []
        for k in self._requiredTags:
            for t in k.split(" or "):
                if t not in ignoreField and t in self._raw.keys():
                    s += "  {tag:{pad}} = {{{val}}},\n".format(pad=sizeMax, tag=t, val=string_to_latex(self._raw[t]))
                    includedTags.append(t)
        
        for k in self._optionalTags:
            for t in k.split(" or "):
                if t not in ignoreField and t in self._raw.keys():
                    s += "  {tag:{pad}} = {{{val}}},\n".format(pad=sizeMax, tag=t, val=string_to_latex(self._raw[t]))
                    includedTags.append(t)
                    
        for t in self._raw.keys():
            if t not in ignoreField and t not in includedTags:
                s += "  {tag:{pad}} = {{{val}}},\n".format(pad=sizeMax, tag=t, val=string_to_latex(self._raw[t]))
                
        return s[:-2]+'\n}'


class Article(BaseEntry):
    """An article from a journal or magazine."""
    _requiredTags = [ 'author', 'title', 'journal', 'year', 'volume' ]
    _optionalTags = [ 'number', 'pages', 'month', 'doi', 'note', 'key' ]

class Book(BaseEntry):
    """A book with an explicit publisher."""
    _requiredTags = [ 'author or editor', 'title', 'publisher', 'year' ]
    _optionalTags = [ 'volume or number', 'series', 'address', 'edition', 'month', 'note', 'key', 'url' ]

class Booklet(BaseEntry):
    """A work that is printed and bound, but without a named publisher or sponsoring institution."""
    _requiredTags = [ 'title' ]
    _optionalTags = [ 'author', 'howpublished', 'address', 'month', 'year', 'note', 'key' ]

class Conference(BaseEntry):
    """The same as inproceedings, included for Scribe compatibility."""
    _requiredTags = [ 'author', 'title', 'booktitle', 'year' ]
    _optionalTags = [ 'editor', 'volume or number', 'series', 'pages', 'address', 'month', 'organization', 'publisher', 'note', 'key' ]

class InBook(BaseEntry):
    """A part of a book, usually untitled. May be a chapter (or section, etc.) and/or a range of pages."""
    _requiredTags = [ 'author or editor', 'title', 'chapter or pages', 'publisher', 'year' ]
    _optionalTags = [ 'volume or number', 'series', 'type', 'address', 'edition', 'month', 'note', 'key' ]

class InCollection(BaseEntry):
    """A part of a book having its own title."""
    _requiredTags = [ 'author', 'title', 'booktitle', 'publisher', 'year' ]
    _optionalTags = [ 'editor', 'volume or number', 'series', 'type', 'chapter', 'pages', 'address', 'edition', 'month', 'note', 'key' ]

class InProceedings(BaseEntry):
    """An article in a conference proceedings."""
    _requiredTags = [ 'author', 'title', 'booktitle', 'year' ]
    _optionalTags = [ 'editor', 'volume or number', 'series', 'pages', 'address', 'month', 'organization', 'publisher', 'note', 'key' ]

class Manual(BaseEntry):
    """Technical documentation."""
    _requiredTags = [ 'title' ]
    _optionalTags = [ 'author', 'organization', 'address', 'edition', 'month', 'year', 'note', 'key' ]

class MastersThesis(BaseEntry):
    """A Master's thesis."""
    _requiredTags = [ 'author', 'title', 'school', 'year' ]
    _optionalTags = [ 'type', 'address', 'month', 'note', 'key' ]

class Misc(BaseEntry):
    """For use when nothing else fits."""
    _requiredTags = [ ]
    _optionalTags = [ 'author', 'title', 'howpublished', 'month', 'year', 'note', 'key' ]

class PhdThesis(BaseEntry):
    """A Ph.D. thesis."""
    _requiredTags = [ 'author', 'title', 'school', 'year' ]
    _optionalTags = [ 'type', 'address', 'month', 'note', 'key' ]

class Proceedings(BaseEntry):
    """The proceedings of a conference."""
    _requiredTags = [ 'title', 'year' ]
    _optionalTags = [ 'editor', 'volume or number', 'series', 'address', 'month', 'publisher', 'organization', 'note', 'key' ]
    
class Talk(BaseEntry):
    """(non-standard) A presentation such as an invited talk."""
    _requiredTags = [ 'author', 'title', 'year', 'month' ]
    _optionalTags = [ 'booktitle', 'note', 'key' ]

class TechReport(BaseEntry):
    """A report published by a school or other institution, usually numbered within a series."""
    _requiredTags = [ 'author', 'title', 'institution', 'year' ]
    _optionalTags = [ 'type', 'number', 'address', 'month', 'note', 'key' ]

class Unpublished(BaseEntry):
    """A document having an author and title, but not formally published."""
    _requiredTags = [ 'author', 'title', 'note' ]
    _optionalTags = [ 'month', 'year', 'key' ]
    
class Workshop(BaseEntry):
    """(non-standard) A workshop presentation."""
    _requiredTags = [ 'author', 'title', 'year', 'month' ]
    _optionalTags = [ 'booktitle', 'note', 'key' ]

class Entry:
    #: Dictionary stores entry type to class mapping
    __typeMap = {'article': Article,
                 'book': Book,
                 'booklet': Booklet,
                 'conference': Conference,
                 'inbook': InBook,
                 'incollection': InCollection,
                 'inproceedings': InProceedings,
                 'manual': Manual,
                 'mastersthesis': MastersThesis,
                 'misc': Misc,
                 'phdthesis': PhdThesis,
                 'proceedings': Proceedings,
                 'talk': Talk,
                 'techreport': TechReport,
                 'unpublished': Unpublished,
                 'workshop': Workshop}

    def __new__(cls, data):
        if 'ENTRYTYPE' in data:
            type = data['ENTRYTYPE'].lower()
            if type in cls.__typeMap:
                return cls.__typeMap[type](data)
            else:
                raise KeyError('Unknown entry type: ' + data['ENTRYTYPE'])
        else:
            print(data)
            raise KeyError('Missing ENTRYTYPE field')
