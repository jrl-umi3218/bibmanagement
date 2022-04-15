from Fields.StringField import StringField
from Fields.NumericField import NumericField


class Address(StringField):
    """Publisher's address (usually just the city, but can be the full address for lesser-known publishers)"""
    pass

class Annote(StringField):
    """"An annotation for annotated bibliography styles (not typical)"""
    pass

class Chapter(NumericField):
    """The chapter number"""
    pass

class Crossref(StringField):
    """The key of the cross-referenced entry"""
    pass

class Doi(StringField):
    """digital object identifier"""
    pass

class Edition(StringField):
    """The edition of a book, long form (such as "First" or "Second")"""
    pass

class Editor(StringField):
    """The name(s) of the editor(s)"""
    pass

class HowPublished(StringField):
    """How it was published, if the publishing method is nonstandard"""
    pass

class Institution(StringField):
    """The institution that was involved in the publishing, but not necessarily the publisher"""
    pass

class Note(StringField):
    """Miscellaneous extra information"""
    pass

class Number(NumericField):
    """The "(issue) number" of a journal, magazine, or tech-report, if applicable. Note that this is not the "article number" assigned by some journals."""
    pass

class Organization(StringField):
    """The conference sponsor"""
    pass

class Publisher(StringField):
    """The publisher's name"""
    pass

class School(StringField):
    """The school where the thesis was written"""
    pass

class Series(StringField):
    """The series of books the book was published in (e.g. "The Hardy Boys" or "Lecture Notes in Computer Science")"""
    pass

class Title(StringField):
    """The title of the work"""
    pass
    
class Todo(StringField):
    """(non-standard) Todo comment for the entry."""
    pass

class Type(StringField):
    """The field overriding the default type of publication (e.g. "Research Note" for techreport, "{PhD} dissertation" for phdthesis, "Section" for inbook/incollection)"""
    pass

class Volume(NumericField):
    """The volume of a journal or multi-volume book"""
    pass

class Year(NumericField):
    """The year of publication (or, if unpublished, the year of creation)"""
    pass
