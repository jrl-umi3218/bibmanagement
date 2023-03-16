# Copyright 2019-2022 CNRS-AIST JRL

from bibmanagement.Entry import *
from bibmanagement.fields import Booktitle
from bibmanagement.fields import Journal
from bibmanagement import log
import yaml
import unicodedata

logger = log.getBibLogger(__name__)

#from https://stackoverflow.com/a/517974
def removeAccents(s):
    nfkd_form = unicodedata.normalize('NFKD', s)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
    
def removeHyphens(s):
    return ''.join(s.split('-'))
    
def removeSpaces(s):
    return ''.join(s.split(' '))
    
def cleanAscii(s):
    return removeSpaces(removeHyphens(removeAccents(s)))

def extractAbbrFromCrossRef(c):
    s = str(c).lower().split(':')
    if len(s) != 2 and len(s) != 3:
        logger.warning(c, 'incorrect_key_format')
        return None
    return s[1]
    
def extractYearFromCrossRef(c):
    s = str(c).lower().split(':')
    if len(s) != 3:
        logger.warning(c, 'incorrect_key_format_conf')
        return None
    return s[2]
    
def getJournalAbbr(j, e):
    j = str(j)
    v = Journal.Journal.getVector(j)
    if v and 'abbr' in v.keys():
        return v['abbr'].lower()
    else:
        logger.warning(e, 'no_abbreviation', {'pub': 'journal', 'name': j})    
        return None
        
def getConferenceAbbr(b, e):
    b = str(b)
    v = Booktitle.Booktitle.getVector(b)
    if v and 'abbr' in v.keys():
        return v['abbr'].lower()
    else:
        logger.warning(e, 'no_abbreviation', {'pub': 'booktitle', 'name': b})
        return None

def extractProceedingsAbbr(e):
    if isinstance(e, (Book, InBook)):
        return 'book'
    if isinstance(e, InProceedings):
        if 'booktitle' in e.keys():
            abbr = getConferenceAbbr(e.booktitle, e)
            if abbr:
                return abbr
        # If we cannot find the booktitle abbreviation, we look at the crossref
        if 'crossref' in e.keys():
            return extractAbbrFromCrossRef(e['crossref'])
        return None
    if isinstance(e, Article):
        if 'journal' in e.keys():
            abbr = getJournalAbbr(e.journal, e)
            if abbr:
                return abbr
        # If we cannot find the journal abbreviation, we look at the crossref
        if 'crossref' in e.keys():
            return extractAbbrFromCrossRef(e['crossref'])
        return None
        
def getFirstAuthorLastName(e):
    if 'author' in e._requiredTags:
        if not 'author' in e.keys():
            logger.warning(e, 'no_author')
            return None
        return e.author[0].last.lower()
    return None
    
def getYear(e):
    if 'year' in e.keys():
        return str(e.year)
    else:
        if isinstance(e, InProceedings) and 'crossref' in e.keys():
            return extractYearFromCrossRef(e['crossref'])
    return None
    
def generatePublicationKey(e):
    name = cleanAscii(getFirstAuthorLastName(e))
    abbr = extractProceedingsAbbr(e)
    year = getYear(e)
    
    if not (name and abbr and year):
        logger.warning(e, 'failed_to_generate_key')
        return None
    
    return ':'.join([name, abbr, year])
    
def generateProceedingsKey(e):
    if 'journal' in e.keys():
        abbr = getJournalAbbr(e.journal, e)
        if abbr:
            return 'jrnl:' + abbr
    if 'booktitle' in e.keys():
        abbr = getConferenceAbbr(e.booktitle, e)
        year = getYear(e)
        if abbr and year:
            return ':'.join(['conf', abbr, year])   

    logger.warning(e, 'failed_to_generate_key')
    
    
def checkKeys(bib):
    for e in bib.entries:
        try:
            if isinstance(e, (Book, InBook, Article, InProceedings)):
                k = generatePublicationKey(e)
                if k != e.id and k != e.id[0:-1]:
                    logger.info(e, 'non_canonical_key', k)
            elif isinstance(e, Proceedings):
                k = generateProceedingsKey(e)
                if k != e.id:
                    logger.info(e, 'non_canonical_key', k)
            else:
                logger.warning(e, 'skipping_key_check')
        except:
            logger.error(e, 'error', e.raw())
