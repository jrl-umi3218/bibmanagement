# Copyright 2019-2022 CNRS-AIST JRL

from bibmanagement.bibParser import *
from bibmanagement.Entry import *
from bibmanagement.fields import Date
from bibmanagement.fields import FormatExpr
from bibmanagement.fields import StringField
from bibmanagement.fields import Authors
from bibmanagement.fields import Pages
from bibmanagement.fields import Journal
from bibmanagement.formatExpr import Parser
from bibmanagement import Biblio
from bibmanagement.utils import StyleFilters as sf

def test():
    db = openBib('tests/data/AE.bib')
    e1 = Entry(db.entries[0])
    print(e1.id)

    class Env: pass
    env = Env()
    env.data = e1
    env.defaultFormat = {}
    env.defaultStyle = {}

    parser = Parser.Parser()
    for i in range(0,1):
        env.data = Entry(db.entries[i])
        r = parser.run(r"[{%First% %Last%}{, }{ and }{1!}]%author%<?, ?>[i][]%title%<?, ?>{%booktitle%|%journal%}<?, ?>%year%", env)
        print(r)

def testExcel():
    bib = Biblio.Biblio.fromBibFile('tests/data/AE.bib')
    bib.toExcel({'B':'[{%F%. %Last%}{, }{ and }{2}]%author%', 'C':'[i][]%title%', 'D':'[u][]%booktitle%|[b][]%journal%', 'E': '%year%'}, 3)
    
def testWord():
    bib = Biblio.Biblio.fromBibFile('tests/data/AE.bib')
    fields.Journal.Journal.readVectorList('C:/work/admin/JRLPubli/journal.json')
    fields.Booktitle.Booktitle.readVectorList('C:/work/admin/JRLPubli/conferences.json')
    bib.toWord(r"[Calibri][{%First% %Last%}{, }{ and }{1!}]%author%<?, ?>[i][]%title%<?, ?>{[u][%iso%]%booktitle%|[b][%abbr%]%journal%}<?, ?>%year%")

def testFilter():
    def in2009(e):
        return int(str(e.format('%year%')))==2009

    fields.Journal.Journal.readVectorList('C:/work/admin/JRLPubli/journal.json')
    fields.Booktitle.Booktitle.readVectorList('C:/work/admin/JRLPubli/conferences.json')
    bib = Biblio.Biblio.fromBibFile('tests/data/AE.bib').filter(in2009)
    bib.toWord(r"[Calibri][{%First% %Last%}{, }{ and }{1!}]%author%<?, ?>[i][]%title%<?, ?>{[u][%iso%]%booktitle%|[b][%abbr%]%journal%}<?, ?>%year%")

def testStyleFilters():
    bib = Biblio.Biblio.fromBibFile('tests/data/AE.bib')
    bib.sort([('%year%','>'), '%booktitle%?2|1'])
    fields.Journal.Journal.readVectorList('C:/work/admin/JRLPubli/journal.json')
    fields.Booktitle.Booktitle.readVectorList('C:/work/admin/JRLPubli/conferences.json')
    boldAK = sf.Filter(type='author', contains='A. Kheddar', bold=True)
    bib.toWord(r"[Calibri][{%F% %Last%}{, }{ and }{}]%author%<?, ?>[i][]%title%<?, ?>{[u][%iso%]%booktitle%|[b][%abbr%]%journal%}<?, ?>%year%", [boldAK])

def testBasicYaml():
    bib = Biblio.Biblio.fromBibFile('tests/data/AE.bib')
    for e in bib.entries:
        print(e.format(("- id: %ID%\n"
                        "  year: %year%\n"
                        "  title: %title%\n"
                        "  booktitle: {%booktitle%|%journal%}\n"
                        "  authors:\n[{    - family: %Last%\n      given : %First%}{\n}{}{}]%author%\n"
                        "<  pdf : ?>%pdf%|%url%<?\n>")))

def testDot():
    bib = Biblio.Biblio.fromBibFile('tests/data/AE.bib')
    e = bib.entries[0]
    print(e.format("%month._date%?range|no range"))

def main():
    #test()
    #testExcel()
    #testWord()
    #testFilter()
    #testStyleFilters()
    #testBasicYaml()
    testDot()

if __name__ == "__main__":
    main()

