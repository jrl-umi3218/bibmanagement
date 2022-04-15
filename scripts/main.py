from bibParser import *
from Entry import *
import Fields.Date
import Fields.FormatExpr
import Fields.StringField
import Fields.Authors
import Fields.Pages
import Fields.Journal
import FormatExpr.Parser as Parser
import Biblio
import utils.StyleFilters as sf

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
    bib.toExcel(3,{'B':'[{%F%. %Last%}{, }{ and }{2}]%author%', 'C':'[i][]%title%', 'D':'[u][]%booktitle%|[b][]%journal%', 'E': '%year%'})
    
def testWord():
    bib = Biblio.Biblio.fromBibFile('tests/data/AE.bib')
    Fields.Journal.Journal.readVectorList('C:/work/admin/JRLPubli/journal.json')
    Fields.Booktitle.Booktitle.readVectorList('C:/work/admin/JRLPubli/conferences.json')
    bib.toWord(r"[Calibri][{%First% %Last%}{, }{ and }{1!}]%author%<?, ?>[i][]%title%<?, ?>{[u][%iso%]%booktitle%|[b][%abbr%]%journal%}<?, ?>%year%")

def testFilter():
    def in2009(e):
        return int(str(e.format('%year%')))==2009

    Fields.Journal.Journal.readVectorList('C:/work/admin/JRLPubli/journal.json')
    Fields.Booktitle.Booktitle.readVectorList('C:/work/admin/JRLPubli/conferences.json')
    bib = Biblio.Biblio.fromBibFile('tests/data/AE.bib').filter(in2009)
    bib.toWord(r"[Calibri][{%First% %Last%}{, }{ and }{1!}]%author%<?, ?>[i][]%title%<?, ?>{[u][%iso%]%booktitle%|[b][%abbr%]%journal%}<?, ?>%year%")

def testStyleFilters():
    bib = Biblio.Biblio.fromBibFile('tests/data/AE.bib')
    bib.sort([('%year%','>'), '%booktitle%?2|1'])
    Fields.Journal.Journal.readVectorList('C:/work/admin/JRLPubli/journal.json')
    Fields.Booktitle.Booktitle.readVectorList('C:/work/admin/JRLPubli/conferences.json')
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

    #Fields.Date.test01()
    #Fields.Date.test02()
    #Fields.FormatExpr.test01()
    #Fields.Authors.test01()
    #Fields.Pages.test01()

    #d = Fields.Date.Date('Jan 31 - Feb 2')
    #print(d.format('%Month% %day1%[-]%day2%'))

    #test()
    #testExcel()
    #testWord()
    #testFilter()
    #testStyleFilters()
    #testBasicYaml()
    testDot()

if __name__ == "__main__":
    main()

