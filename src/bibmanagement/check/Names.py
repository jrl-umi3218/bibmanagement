import Biblio
import Fields.Name
import Check.LevenshteinDistance
import yaml

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
                print('Warning, no author for entry ' + e['ID'])
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
            dist = Check.LevenshteinDistance.distance(s[i][0],s[j][0])
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
            print("possible typo ({}): {} -> {}".format(d, n1, n2) + " ({})  {}".format(s[j][1], l[n1]))

def probableSwitch(bib, distMax = 2, ignoreFile = None):
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
            d1 = Check.LevenshteinDistance.distance(fi,lj)
            d2 = Check.LevenshteinDistance.distance(fj,li)
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
            print("Possible name switch: {} <-> {} ({})".format(n1, n2, s[j][1]) + " {}".format(l[n1]))
            
def possibleAbbreviation(bib, ignoreFile = None):
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
            print("Possible abbreviation: {} {}".format(n,p))
            
    
def all(bib, ignoreFile = None):
    print("check typo")
    probableTypo(bib, 3, ignoreFile)
    print("check switch")
    probableSwitch(bib, 2, ignoreFile)
    print("check abbreviation")
    possibleAbbreviation(bib, ignoreFile)
