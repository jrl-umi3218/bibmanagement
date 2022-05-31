from bibmanagement.fields.StringField import StringField
from bibmanagement.fields.NumericField import NumericField


class Abstract(StringField):
    """Abstract of the paper"""
    pass

class Acmid(NumericField):
    """ID as given by ACM"""
    pass

class Hal_id(StringField):
    """ID as given by the HAL repository"""
    pass

class Hal_version(NumericField):
    """"Version on HAL"""
    @classmethod
    def _fromString(cls, str):
        assert(str[0]=='v')
        return cls(int(str[1:]))

class Keywords(StringField):
    """Keywords attached to the paper, coma- or semi-colon- separated"""

class Pdf(StringField):
    """url of the pdf (specifically)"""
    pass

class Url(StringField):
    """url where to find the pdf or a page leading tho the pdf"""
    pass
    
class Lab(StringField):
    """lab affiliation, to specify if the paper is affiliated to JRL"""
    pass
    
class Isbn(StringField):
    """International Standard Book Number"""
    pass
    
class Todo(StringField):
    """todo remarks"""
    pass