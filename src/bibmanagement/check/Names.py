from bibmanagement import Biblio
from bibmanagement.fields import Name
from bibmanagement.check import LevenshteinDistance
from bibmanagement import log
import logging
import yaml

logger = log.getBibLogger(__name__)

#TODO: we are using a ad hoc system based on an ignoreFile, whose role is to
# discard false positive outputs of the functions in this module.
# The newer logging system with its own discard mechanism is offering an 
# alternative, more generic solution. We could thus remove all the code
# related to the ignoreFile.

def checkLogger():
    """
    By default the bibmanagement logger logs message for the level INFO and
    above, but the default Handler (logging.lastResort) only prints out logs
    with level WARNING and above.
    We don't want to change the behavior of the default Handler, to avoid the
    bibmanagement package to be intrusive. This method warns the user that
    some useful logs emitted by the current module might be discarded.
    """
    
    packageLogger = logging.getLogger('bibmanagement')
    rootLogger = logging.getLogger()
    if not packageLogger.handlers and not rootLogger.handlers and not logger.handlers and logging.lastResort.level > logging.INFO:
        logger.warning(None, 'generic', 
'''
!Warning!
Methods in bibmanagement.check.Names rely on emitting log at the logging.INFO
level. With the current logging configuration, these logs might not be
displayed. This is in particular the case if you are using the default logging
configuration.

To correct this, the simpler solution is to perform the following:
    from bibmanagement import log
    log.setupSelectHandler()
    
Otherwise, if you know how the logging library works in python, you can add
a logging.Handler that accepts logging.INFO level to the root logger, the
\'bibmanagement.check.Names\' logger or any of its ancestor.
''')

def listNames(bib, mode='both'):
    l = {}
    if mode == 'first':
        render = lambda x: x.first.lower()
    elif mode == 'last':
        render = lambda x: x.last.lower()
    elif mode == 'both':
        render = lambda x: x.first.lower() + ' ' + x.last.lower()
    elif mode == 'separate':
        render = lambda x: (x.first.lower(), x.last.lower())
    else:
        raise ValueError("Unknown mode {}: possible modes are first, last, both or separate".format(mode))
    for e in bib.entries:
        if 'author' in e._requiredTags:
            if not 'author' in e.keys():
                logger.warning(e, 'no_author')
                continue
            for a in e.author:
                name = render(a)
                if name in l:
                    l[name].append(e['ID'])
                else:
                    l[name] = [e['ID']]
                
    return l


def probableTypo(bib, distMax = 2, ignoreFile = None):
    """List the probable typos on the couple (First name, Family name)"""
    checkLogger()
    
    if ignoreFile:
        with open(ignoreFile, encoding='utf8') as file:
            ignore = yaml.load(file, Loader=yaml.FullLoader)
            ignoreName = ignore.get('fullnameTypo',[])
    else:
        ignoreName = []
    
    l = listNames(bib, 'both')
    s = [(k,len(p)) for k,p in sorted(l.items(), key = lambda i: len(i[1]))]
    matches={};
    for i in range(len(s)):
        for j in range(i+1,len(s)):
            dist = LevenshteinDistance.distance(s[i][0],s[j][0])
            if dist<=distMax:
                matches[i] = (j, dist)
                
    for i,k in matches.items():
        j, d = k
        n1 = s[i][0]
        n2 = s[j][0]
        skip = False
        for e in ignoreName:
            if ((n1,n2) == (e['first'],e['second']) or (n2,n1) == (e['first'],e['second'])):
                skip = True
                break
        if not skip:
            logger.info(bib[l[n1][0]], 'possible_typo', n1, n2, additionalMsg =' ({})'.format(s[j][1]))

def probableSwitch(bib, distMax = 2, ignoreFile = None):
    checkLogger()
    
    if ignoreFile:
        with open(ignoreFile, encoding='utf8') as file:
            ignore = yaml.load(file, Loader=yaml.FullLoader)
            ignoreName = ignore.get('switchName', [])
    else:
        ignoreName = []
        
    l = listNames(bib, 'separate')
    s = [(k,len(p)) for k,p in sorted(l.items(), key = lambda i: len(i[1]))]
    matches={};
    for i in range(len(s)):
        fi,li = s[i][0]
        for j in range(i+1,len(s)):
            fj,lj = s[j][0]
            d1 = LevenshteinDistance.distance(fi,lj)
            d2 = LevenshteinDistance.distance(fj,li)
            if d1+d2<=distMax:
                matches[i] = j
                
    for i,j in matches.items():
        n1 = s[i][0]
        n2 = s[j][0]
        skip = False
        for e in ignoreName:
            if ((n1,n2) == (e['first'],e['last']) or (n2,n1) == (e['first'],e['last'])):
                skip = True
                break
        if not skip:
            logger.info(bib[l[n1][0]], 'possible_name_switch', n1, n2, additionalMsg=' ({})'.format(s[j][1]))
            
def possibleAbbreviation(bib, ignoreFile = None):
    checkLogger()
    
    if ignoreFile:
        with open(ignoreFile, encoding='utf8') as file:
            ignore = yaml.load(file, Loader=yaml.FullLoader)
            ignoreName = ignore.get('nameAbbreviation',[])
    else:
        ignoreName = []
    
    l = listNames(bib, 'first')
    l.update(listNames(bib, 'last'))
    for n,p in l.items():
        if (len(n)==1 or (len(n)==2 and n[1]=='.')) and not n in ignoreName:
            logger.info(bib[p[0]], 'possible_abbr', n)
            
    
def all(bib, ignoreFile = None):
    print("check typo")
    probableTypo(bib, 3, ignoreFile)
    print("check switch")
    probableSwitch(bib, 2, ignoreFile)
    print("check abbreviation")
    possibleAbbreviation(bib, ignoreFile)
