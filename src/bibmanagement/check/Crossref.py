from bibmanagement.Entry import Proceedings
from bibmanagement import log

logger = log.getBibLogger(__name__)


def unusedProceedings(bib):
    """ List all proceedings in the bib file that are not crossref'd"""
    used = []
    proc = []
    for e in bib.entries:
        if isinstance(e,Proceedings):
            proc.append(e.id)
        else:
            x = e
            while 'crossref' in x:
                x = bib[str(x.crossref.format())]
                used.append(x.id)
                
    unused = [p for p in proc if p not in used]
    return unused
            
            
def duplicatedFields(bib):
    """
    Returns a pair [d, o], where d is a list of fields that are identical in an entry and its
    crossref, and o is a list of fields that are found both in an entry and its crossref but are
    not identical.
    Each elements of d or o is a quintuple (id_e, id_c, fieldname, value_e, value_c) where
    id_e is the bib key of the entry
    id_c is the bib key of its crossref
    fieldname is the name of the field that is found in both the entry and the crossref
    value_e is the value of the field for the entry
    value_c is the value of the field for the crossref.
    """
    overwriten = []
    duplicate = []
    # we assume a single level of crossref
    for e in bib.entries:
        if 'crossref' in e:
            c = bib[str(e.crossref.format())]
            if 'crossref' in c:
                logger.warning(e, 'chained_crossref', c.id)
            for f in c:
                if f not in ['ID', 'title', 'crossref'] and f in e:
                    cf = str(c[f].format())
                    ef = str(e[f].format())
                    if ef.lower() == cf.lower():
                        duplicate.append((e.id, c.id, f, ef, cf))
                    else:
                        overwriten.append((e.id, c.id, f, ef, cf))
                        
    return [duplicate, overwriten]
