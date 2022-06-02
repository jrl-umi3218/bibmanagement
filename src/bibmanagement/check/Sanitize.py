import sys 
sys.path.append('..')

import bibParser
import Biblio
import Check.Crossref
import Check.Order
from functools import cmp_to_key

def getInteractiveInput(d):
    print(d)
    val = ''
    while val not in ['k', 'd', 'c']:
        val = input('(k)eep, (d)elete or keep for later (c)heck: ').lower()
    return val

def removeFromEntry(e, dupl, interactive=False):
    k = Check.Order.getKey(e)
    lines = []
    cpt = 0
    fields = {d[2]:i for (i,d) in enumerate(dupl) if d[0] == k}
    for l in e[1].splitlines():
        s = l.split('=')[0].strip().lower()
        if s in fields.keys():
            if interactive:
                d = dupl[fields[s]]
                i = getInteractiveInput(d)
                if i == 'k':
                    lines.append(l)
                elif i == 'c':
                    lines.append(l)
                    removeFromEntry.check.append(d)
                else:
                    cpt = cpt + 1
            else:     # we skip this line
                cpt = cpt + 1
        else:
            lines.append(l)
    if cpt>0:
        lines.append('')
        return [(e[0], '\n'.join(lines)), cpt]
    else:
        return [e, 0]
                

def removeDuplicatedFields(entries, dupl, interactive=False):
    """ 
    Remove from entries the field that are duplicates from those of their crossrefs.
    
    entries is a list of string as return by bibParser.rawEntries
    dupl is a list of duplicates as returned by Crossref.duplicatedFields
    """

    out = []
    cpt = 0
    removeFromEntry.check = []
    
    for e in entries:
        if e[0].lower() == 'string':
            out.append(e)
        else:
            [r, c] = removeFromEntry(e, dupl, interactive)
            out.append(r)
            cpt = cpt + c
            
    print("Removed {} duplicated fields".format(cpt))
    if interactive:
        print('fields to check:')
        print(removeFromEntry.check)
    return out
    
    
def removeUnecessaryProceedings(entries, unused):
    """Remove the proceedings that are not crossref'd"""
    keep = []
    discard = []
    
    for e in entries:
        k = Check.Order.getKey(e)
        if k in unused:
            discard.append(e)
        else:
            keep.append(e)
            
    return (keep, discard)
        
    
def writeEntry(f, e):
    if e[0].lower() != 'string':
        f.write('\n')
    f.write('@' + e[0] + '{')
    f.write(e[1])
    f.write('}\n')
    
def removeUnecessary(inFile, outFile, fields = True, entries = False, unusedEntryFile=''):
    """
    From an input file, write a new file where (some) unecessary data have been removed.
    
    If fields is True, remove the entry fields that are identical to the same fields in a crossref.
    If entries = True, remove the proceedings entries that are not crossref'd.
    If a path is given by unusedEntryFile, the proceedings removed will be copied to this file.
    
    Todo: we do not pay attention to preamble strings for now. We should remove those that are only
    used by removed entries. Possibly, all necessary strings should be copied into the unusedEntryFile.
    """
    encoding = bibParser.getEncoding(inFile)
    bib = Biblio.Biblio.fromBibFile(inFile)
    e = bibParser.rawEntries(inFile)
    
    if fields:
        [dupl, over] = Check.Crossref.duplicatedFields(bib)
        e = removeDuplicatedFields(e, dupl)
        
    if entries:
        unused = Check.Crossref.unusedProceedings(bib)
        [e, discard] = removeUnecessaryProceedings(e, unused)
        if unusedEntryFile:
            with open(unusedEntryFile, 'w', encoding=encoding) as f:
                for entry in discard:
                    writeEntry(f, entry)
            
        
    with open(outFile, 'w', encoding=encoding) as f:
        for entry in e:
            writeEntry(f, entry)
            
            
def reorder(inFile, outFile):
    """ Reorder the items in the input file according to the order given by Check.Order.cmpRawEntries"""
    encoding = bibParser.getEncoding(inFile)
    e = bibParser.rawEntries(inFile)
    e.sort(key=cmp_to_key(Check.Order.cmpRawEntries))
    
    with open(outFile, 'w', encoding=encoding) as f:
        for entry in e:
            writeEntry(f, entry)
            

def removeOverwrittenFields(inFile, outFile):
    """
    """
    encoding = bibParser.getEncoding(inFile)
    bib = Biblio.Biblio.fromBibFile(inFile)
    e = bibParser.rawEntries(inFile)

    [dupl, over] = Check.Crossref.duplicatedFields(bib)
    e = removeDuplicatedFields(e, over, True)
              
    with open(outFile, 'w', encoding=encoding) as f:
        for entry in e:
            writeEntry(f, entry)
            