import sys 
sys.path.append('..')
import bibParser

def stringKey(e):
    return e[1].split('=')[0].strip().lower()
    
def cmpVal(s1,s2):
    if s1<s2:
        return -1
    elif s1>s2:
        return 1
    else:
        return 0
        
def cmpType(t1,t2):
    """
    Compare two entry types using the following order:
    article < inproceedings < others type by alphabetical order < proceedings < collection < comment
    """
    if not hasattr(cmpType, "order"):
        cmpType.order = {'article':0, 'inproceedings':1, 'proceedings':3, 'collection': 4, 'comment':5} # 2 is other values
    
    s1 = cmpType.order.get(t1.lower(), 2)
    s2 = cmpType.order.get(t2.lower(), 2)
    
    if s1 == 2 and s2 == 2:
        return cmpVal(t1,t2) # we compare t1 and t2 lexicographically
    else:
        return cmpVal(s1, s2) # we compare t1 and t2 based on s1 and s2

def getKey(e):
    return e[1].split(',')[0].strip().lower()
    
def asYear(s):
    """
    If s is a 4 digits number in string form yyyy, possibly followed by an additional character c,
    returns the pair (yyyy, c). Otherwise, returns ('','') 
    """
    n = len(s)
    if n <4 or n>5:
        return ('','')
    else:
        if s[0:4].isnumeric():
            return (s[0:4], s[4:n])
        else:
            return ('', '')
    
def splitAndReorderKey(k):
    s = k.lower().split(':')
    s.reverse()
    [y,c] = asYear(s[0])
    if y and c:
        s[-1] = s[-1] + c
        s[0] = y
    if len(s) == 3:
        if s[2]=='conf':
            # For conf we want to order by name first and the year
            tmp = s[0]
            s[0] = s[1]
            s[1] = tmp
        return s
    if len(s) == 2 and (s[1] == 'jrnl' or s[1] == 'book'):
        return s
    else:
        raise ValueError('Ill-formed key: {}'.format(k))
        

def cmpRawEntries(e1, e2):
    """ 
    A comparison between entries which puts the preamble strings first, then sort by entry type,
    year, proceedings' name and first author's name.
    """
    if e1[0].lower() == 'string':
        if e2[0].lower() == 'string':
            return cmpVal(stringKey(e1), stringKey(e2))
        else:
            return -1
    else:
        if e2[0].lower() == 'string':
            return 1
        else:
            # both entries are not preamble strings
            # we first compare their type 
            ct = cmpType(e1[0], e2[0])
            if ct != 0:
                return ct
            # entries have the same type, we now compare the keys
            try:
                s1 = splitAndReorderKey(getKey(e1))
                s2 = splitAndReorderKey(getKey(e2))
            except ValueError as ve:
                raise ValueError('{}\n for \n e1 = \n {} \n and e2 = \n {}'.format(ve,e1,e2))
            return cmpVal(s1, s2)
            

# e = bibParser.rawEntries(...)
# e.sort(key=cmp_to_key(Check.Order.cmpRawEntries))