from bibmanagement.Fields.StringField import StringField
from bibmanagement.utils.FormattedString import Single
from bibmanagement.log import logging
import json
import sys

logger = logging.getBibLogger(__name__)

class PublicationVector(StringField):
    # list of vectors of publication (i.e. journal, proceeddings,...)
    _vectorList = {}

    _defaultFormatExpr = '%Name%'

    @staticmethod
    def readVectorList(filepath):
        '''
        Read a json file and add its content to _vectorList. 
        
        Note that this does not reset _vectorList so that several files can be appended.'''
        with open(filepath, encoding="utf-8") as json_file:
            data = json.load(json_file)
            
            for d in data:
                name = d.get('name')
                if name:
                    if name in PublicationVector._vectorList:
                        logger.info(None, 'pub_already_present', name)
                    PublicationVector._vectorList[name] = d
                else:
                    raise ValueError('No name field in item ' + str(d))
                    
    @staticmethod
    def resetVectorList():
        '''
        Erase all the entries in the vector list
        '''
        PublicationVector._vectorList = {}

    @staticmethod
    def getVector(name):
        v = PublicationVector._vectorList.get(name)
        if v:
            return v
        else:
            #we start looking for alternative names
            for v in PublicationVector._vectorList.values():
                if name.lower() == v.get('name','').lower(): return v
                alt = v.get('alternative',[])
                for a in alt:
                    if a.lower() == name.lower():
                        return v
                #we check the abbreviations
                if name.lower() == v.get('abbr','').lower(): return v
                if name.lower() == v.get('iso','').lower() : return v
                if name.lower() == v.get('jcr','').lower() : return v

        return None

    @staticmethod
    def getName(vectorName, nameType):
        nt = nameType.lower()
        v = PublicationVector.getVector(vectorName)
        if v:
            n = v.get(nt)
            if n:
                return n
            else:
                logger.warning(None, 'not_in_data', nameType, vectorName)
                return vectorName
        else:
            logger.warning(None, 'not_in_vector', vectorName)
            return vectorName


    def _format(self, formatExpr, style):
        n = formatExpr.count('%')
        if n != 2:
            raise ValueError('Format expr must include exactly one placeholder (enclosed by %)')
        fe = formatExpr.split('%')
        ph = fe[1]

        name = PublicationVector.getName(self._val, ph)
        s = formatExpr.replace('%'+ph+'%', name)

        return Single(self.__class__.__name__.lower(),s, style)
        
    def international(self):
        v = PublicationVector.getVector(self._val)
        if v:
            nat = v.get('national','')
            if nat=='':
                raise ValueError('Missing \'national\' field for ' + self._val + ' in vector list.')
            return not nat
        else:
            raise ValueError('Cannot find ' + self._val + ' in vector list. Cannot determine its international character.')
            
    def get(self, prop, default=None, errorIfMissing=True):
        v = PublicationVector.getVector(self._val)
        if v:
            if prop in v:
                return v[prop]
            else:
                msg = "Publication {0} does not have entry {1}".format(self._val, prop)
                if errorIfMissing:
                    raise ErrorValue(msg)
                else:
                    logger.warning(None, 'generic', msg)
                    return default
        else:
            msg = "Cannot find {0} in vector list. Cannot determine the value of {1}.".format(self._val, prop)
            if errorIfMissing:
                raise ValueError(msg)
            else:
                logger.warning(None, 'generic', msg)
                return default
            


class Journal(PublicationVector):
    """The journal or magazine the work was published in"""
    pass
