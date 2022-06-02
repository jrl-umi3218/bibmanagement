from bibmanagement.Entry import *
import bibmanagement.fields.Name
import bibmanagement.check.LevenshteinDistance
import yaml
import unicodedata

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
        print('Warning, crossref value does not have the form jrnl:abbr or conf:abbr:year')
        return None
    return s[1]
    
def extractYearFromCrossRef(c):
    s = str(c).lower().split(':')
    if len(s) != 3:
        print('Warning, crossref value does not have the form conf:abbr:year')
        return None
    return s[2]
    
def getJournalAbbr(j, e):
    j = str(j)
    v = Fields.Journal.Journal.getVector(j)
    if v and 'abbr' in v.keys():
        return v['abbr'].lower()
    else:
        print('Not able to find journal {} or this journal does not have an abbreviation (entry {})'.format(j, e['ID']))    
        return None
        
def getConferenceAbbr(b, e):
    b = str(b)
    v = Fields.Booktitle.Booktitle.getVector(b)
    if v and 'abbr' in v.keys():
        return v['abbr'].lower()
    else:
        print('Not able to find booktitle {} or this booktitle does not have an abbreviation (entry {})'.format(b, e['ID']))
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
            print('Warning, no author for entry {}'.format(e['ID']))
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
        print('Warning, unable to generate key for entry {}'.format(e['ID']))
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

    print('Warning, unable to generate key for entry {}'.format(e['ID']))
    
    
def checkKeys(bib):
    for e in bib.entries:
        try:
            if isinstance(e, (Book, InBook, Article, InProceedings)):
                k = generatePublicationKey(e)
                if k != e.id and k != e.id[0:-1]:
                    print('Entry {} should have key {}'.format(e.id, k))
            elif isinstance(e, Proceedings):
                k = generateProceedingsKey(e)
                if k != e.id:
                    print('Entry {} should have key {}'.format(e.id, k))
            else:
                print('Not checking for {}'.format(e.id))
        except:
            print(e.raw())
