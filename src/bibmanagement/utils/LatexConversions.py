from bibmanagement import log
from bibtexparser.latexenc import latex_to_unicode
import re

logger = log.getBibLogger(__name__)

def latex_to_unicode_preserve_formula(s, preserve):
    l = s.split('$')
    if not preserve or len(l)%2 == 0:
        return latex_to_unicode(s)
    else:
        converted = [latex_to_unicode(si) if i%2==0 else si for i,si in enumerate(l)]
        return '$'.join(converted)
    

def _convert_to_unicode_preserve_formula(record, preservedFields):
    for val in record:
        preserve = val in preservedFields
        if isinstance(record[val], list):
            record[val] = [
                latex_to_unicode_preserve_formula(x, preserve) for x in record[val]
            ]
        elif isinstance(record[val], dict):
            record[val] = {
                k: latex_to_unicode_preserve_formula(v, preserve) for k, v in record[val].items()
            }
        else:
            record[val] = latex_to_unicode_preserve_formula(record[val], preserve)
    return record
    
def convert_to_unicode_preserve_formula(preservedFields = None):
    def f(record):
        return _convert_to_unicode_preserve_formula(record, preservedFields)
    return f

def parse_braces(s):
    """
    Compute a nested list corresponding to the structure givem by the braces
    
    For example 'This {is} a {test {for {{nested} braces}}.}'
    gives ['This ', ['is'], ' a ', ['test ', ['for ', [['nested'], ' braces']], '.']]
    """
    l = [e.split('}') for e in s.split('{')]
    assert len(l)-1 == sum([len(e) for e in l])-len(l), 'The numbers of opening and closing braces are different.\ninput = {0}'.format(s)
    
    r = []
    stack = [r]
    depth = 0
    for e in l:
        cur = []
        stack.append(cur)
        for i in e:
            if i:
                cur.append(i)
            if i is not e[-1] or e is l[-1]:
                p = stack.pop()
                cur = stack[-1]
                cur.append(p)
    
    return r[0]
    

def _remove_keywords(s):
    expr = re.compile(r"\\\w+")
    while expr.search(s):
        for m in expr.finditer(s):
            s = s.replace(m[0], '')
    return s
            
def _remove_special_char(s):
    s = s.replace('_', '')
    s = s.replace('^', '')
    return s
 
def _remove_formula(s):
    if isinstance(s, str):
        l = parse_braces(s)
        if len(l) == 1:
            if isinstance(l[0], str):
                return _remove_special_char(_remove_keywords(s))
            else:
                return ''.join([_remove_formula(e) for e in l[0]])
        else:
            return ''.join([_remove_formula(e) for e in l])
    else:
        return ''.join([_remove_formula(e) for e in s])
        
def remove_formula(s):
    l = s.split('$')
    if len(l)%2 == 0:
        return s
    else:
        converted = [_remove_formula(si) if i%2==1 else si for i,si in enumerate(l)]
        return _remove_formula(''.join(converted))