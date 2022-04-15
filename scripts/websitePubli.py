from bibParser import *
from Entry import *
import Biblio
import utils.BibFilter
import Fields.Journal
import Fields.Booktitle
import yaml
import os


def generateYamlEntry(e):
    """Given an object of type Entry, generate the corresponding yaml entry for the publication list"""
    try:
        d = {"id": str(e.format("%ID%")),
             "year": e.year._val,
             "title": str(e.format("%title%")),
             "booktitle": str(e.format("{%booktitle%|%journal%}")),
             "authors": [{"family":a.last, "given":a.first} for a in e.author._authors]}
        
        if 'pdf' in e.keys() and e.pdf:
            d['pdf'] = str(e.pdf)
        elif 'url' in e.keys() and e.url:
            d['pdf'] = str(e.url)
        
        if 'project' in e.keys() and e.project:
            d['projects'] = [str.lower(p) for p in e.project._projects]
            
        if 'lab' in e.keys() and e.lab:
            d['lab'] = str.lower(str(e.lab))
            
        return d
    except:
        print(e.raw())

def generateInitialYaml(bibfilePath):
    """Generate the yaml file containing the journal, conference and book articles from the given bib file."""
    bib = Biblio.Biblio.fromBibFile(bibfilePath).resolveCrossref()
    bib = bib.filter(utils.BibFilter.Selector(committee=True))
    select = (Article,InProceedings,Book)
    yamlData = [generateYamlEntry(e) for e in bib.entries if isinstance(e, select)]
    return yamlData
    
def replaceAuthorWithId(author, idList):
    for p in idList:
        if str.lower(author['family']) == str.lower(p['family']) and str.lower(author['given']) == str.lower(p['given']):
            return {"id": p['id']}
            
    return author
    
def replaceNameWithId(yamlData, idFilePath, alternativeNameFilePath):
    with open(idFilePath, encoding='utf8') as file:
        members = yaml.load(file, Loader=yaml.FullLoader)
        
    if alternativeNameFilePath:
        with open(alternativeNameFilePath, encoding='utf8') as file:
            members += yaml.load(file, Loader=yaml.FullLoader)
    
    for e in yamlData:
        e['authors'] = [replaceAuthorWithId(a, members) for a in e['authors']]
        
    return yamlData
    
def addYamlData(to, additionalFilePath):
    with open(additionalFilePath, encoding='utf8') as file:
        add = yaml.load(file, Loader=yaml.FullLoader)
        
    for e in add:
        found = False
        for t in to:
            if str.lower(e['id']) == str.lower(t['id']):
                found = True
                for k,v in e.items():
                    if v:
                        t[k] = v
                    else:
                        del t[k]
                        
                break
        if not found:
            print('Adding entry ' + e['id'])
            to.append(e)
        
    return to
    
def generateYaml(bibfilePath, memberFilePath, journalListPath, conferenceListPath, additionalFilePath = None, alternativeNameFilePath = None, outPath = 'publications.yml'):
    if journalListPath:
        Fields.Journal.Journal.readVectorList(journalListPath)
    if conferenceListPath:
        Fields.Booktitle.Booktitle.readVectorList(conferenceListPath)
    yamlData = generateInitialYaml(bibfilePath)
    yamlData = replaceNameWithId(yamlData, memberFilePath, alternativeNameFilePath)
    if additionalFilePath:
        yamlData = addYamlData(yamlData, additionalFilePath)
    
    os.makedirs(os.path.dirname(outPath), exist_ok=True)
    with open(outPath, 'w', encoding='utf8') as file:
        file.write("################################################################\n"
                   "#                                                              #\n"
                   "#                    W  A  R  N  I  N  G  !                    #\n"
                   "#                                                              #\n"
                   "# This is a automatically generated file, don't edit manually. #\n"
                   "#                                                              #\n"
                   "################################################################\n")
        yaml.dump(yamlData, stream=file, allow_unicode=True, sort_keys=False)    

def generateBib(bibfilePath, outDirPath):
    bib = Biblio.Biblio.fromBibFile(bibfilePath).resolveCrossref()
    bib = bib.filter(utils.BibFilter.Selector(committee=True))
    select = (Article,InProceedings,Book)
    for e in bib.entries:
        bibPath = outDirPath + e.id.replace(':','_')+'.bib'
        if isinstance(e, select):
            try:
                with open(bibPath, 'w') as bib:
                    bib.write(e.toString(['lab','crossref']))
            except Exception as ex:
                print("Error with")
                print(e.raw())
                print(ex)

def generateYamlJRL(jrlPubliPath, jrlWebsitePath, generateEntryBib=False):
    """Example of use:  websitePubli.generateYamlJRL('C:/Work/admin/JRLPubli', 'C:/Work/code/misc/jrl-umi3218.github.com')"""
    if jrlPubliPath[-1] != '/':
        jrlPubliPath += '/'
    if jrlWebsitePath[-1] != '/':
        jrlWebsitePath += '/'
    bibfilePath = jrlPubliPath + 'master.bib'
    journalListPath = jrlPubliPath + 'journal.json'
    conferenceListPath = jrlPubliPath + 'conferences.json'
    additionalFilePath = jrlPubliPath + 'websiteAdditionalData.yml'
    memberFilePath = jrlWebsitePath + '_data/members.yml'
    alternativeNameFilePath = jrlPubliPath + 'alternativeNames.yml'
    outDirPath = jrlPubliPath + 'tmp/'
    outPath = outDirPath + 'publications.yml'
    generateYaml(bibfilePath, memberFilePath, journalListPath, conferenceListPath, additionalFilePath, alternativeNameFilePath, outPath)
    if generateEntryBib:
        generateBib(bibfilePath, outDirPath)
    
def generateMemberPages(memberFilePath, outDirPath = 'tmp/'):
    with open(memberFilePath, encoding='utf8') as file:
        members = yaml.load(file, Loader=yaml.FullLoader)
    
    if outDirPath[-1] != '/':
        outDirPath += '/'
    os.makedirs(outDirPath, exist_ok=True)
    
    for m in members:
        filePath = outDirPath + 'member-' + m['id'] + '.html'
        with open(filePath, 'w', encoding='utf8') as file:
            file.write("---\n"
                       "layout: default\n"
                       "title: CNRS-AIST JRL\n"
                       "---\n"
                       "{% include member_full.html id=\""+ m['id'] + "\" %}\n")
        