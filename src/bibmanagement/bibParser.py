# Copyright 2019-2022 CNRS-AIST JRL

import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibmanagement.utils import LatexConversions
import re

def getEncoding(filePath):
    encodingMap={'utf-8':         'utf8',
                 'utf8':          'utf8',
                 'windows-1252':  'cp1252'}
    with open(filePath, encoding="ascii", errors="surrogateescape") as file:
        l = file.readline().lower()
        while len(l):
            g = re.match(r"\s*%\s*encoding\s*:\s*([\w-]+)", l)
            if g:
                e = g.group(1)
                if e in encodingMap:
                    return encodingMap[e]
                else:
                    msg = 'Found an unknown encoding: ' + e + ' Please consider updating encodingMap.'
                    raise KeyError(msg)
            l = file.readline()
        # return utf8 by default
        return 'utf8'


def openBib(filePath):
    encoding = getEncoding(filePath)
    with open(filePath, encoding=encoding) as bibFile:
        parser = BibTexParser(common_strings=True, ignore_nonstandard_types=False)
        parser.customization = LatexConversions.convert_to_unicode_preserve_formula(['title', 'abstract'])
        return parser.parse_file(bibFile)


def rawEntries(filePath):
    encoding = getEncoding(filePath)
    bracketCount = 0
    inEntries = False
    entries = []
    entryType = ''
    entryData = ''
    accumulate = ''
    state = 0
    with open(filePath, encoding=encoding) as bibFile:
        for line in bibFile:
            for ch in line: 
                if state == 0:
                    if ch == '@':
                        accumulate = ''
                        state = 1
                        continue
                elif state == 1:
                    if ch == '{':
                        bracketCount = 1
                        entryType = accumulate.strip()
                        accumulate = ''
                        state = 2
                        continue
                elif state == 2:
                    if ch == '{':
                        bracketCount = bracketCount + 1
                    elif ch == '}':
                        bracketCount = bracketCount - 1
                    if bracketCount == 0:
                        entries.append((entryType, accumulate))
                        accumulate = ''
                        state = 0
                        continue
                accumulate = accumulate + ch
                
    return entries