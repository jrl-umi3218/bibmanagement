# Copyright 2019-2022 CNRS-AIST JRL

from bibmanagement.bibParser import *
from bibmanagement.Entry import *
from bibmanagement.fields import Date
from bibmanagement.fields import FormatExpr
from bibmanagement.fields import StringField
from bibmanagement.fields import Authors
from bibmanagement.fields import Pages
from bibmanagement.fields import Journal
from bibmanagement.fields import Booktitle
from bibmanagement.formatExpr import Parser
from bibmanagement import Biblio
from bibmanagement.utils import StyleFilters as sf

import unittest
import os

dirPath = os.path.dirname(os.path.abspath(__file__))
dataPath = os.path.join(dirPath, '../data')
outPath = os.path.join(dirPath, '../out')

class TestMain(unittest.TestCase):
    def test_parse(self):
        db = openBib(dataPath + '/AE.bib')
        e1 = Entry(db.entries[0])
        #print(e1.id)

        class Env: pass
        env = Env()
        env.data = e1
        env.defaultFormat = {}
        env.defaultStyle = {}

        parser = Parser.Parser()
        def testEntry(i, output):
            env.data = Entry(db.entries[i])
            r = parser.run(r"[{%First% %Last%}{, }{ and }{1!}]%author%<?, ?>[i][]%title%<?, ?>{%booktitle%|%journal%}<?, ?>%year%", env)
            self.assertEqual(str(r), output)
            
        testEntry(0, 'Hervé Audren et al., Model Preview Control in Multi-Contact Motion -- Application to a Humanoid Robot, IEEE/RSJ International Conference on Intelligent Robots and Systems, 2014')
        
        testEntry(8, 'Adrien Escande, Fast closest logarithm algorithm in the special orthogonal group, IMA Journal of Numerical Analysis, 2016')
        
    def test_excel(self):
        bib = Biblio.Biblio.fromBibFile(dataPath + '/AE.bib')
        bib.toExcel({'B':'[{%F%. %Last%}{, }{ and }{2}]%author%', 'C':'[i][]%title%', 'D':'[u][]%booktitle%|[b][]%journal%', 'E': '%year%'}, 3, out=outPath+'/test')
        
    def test_word(self):
        bib = Biblio.Biblio.fromBibFile(dataPath + '/sample.bib')
        Journal.Journal.readVectorList(dataPath + '/sample_journal.json')
        Booktitle.Booktitle.readVectorList(dataPath + '/sample_conf.json')
        bib.toWord(r"[Calibri][{%First% %Last%}{, }{ and }{1!}]%author%<?, ?>[i][]%title%<?, ?>{[u][%iso%]%booktitle%|[b][%abbr%]%journal%}<?, ?>%year%", out=outPath+'/test')
        
    def test_filter(self):
        def in2009(e):
            return int(str(e.format('%year%')))==2009

        bib = Biblio.Biblio.fromBibFile(dataPath + '/AE.bib').filter(in2009)
        self.assertEqual(len(bib.entries), 7)
        
    def testStyleFilters(self):
        bib = Biblio.Biblio.fromBibFile(dataPath + '/sample.bib')
        bib = bib.resolveCrossref()
        # Sort journals first then conference. Within each type, sort by date.
        bib.sort(['%booktitle%?2|1', ('%year%','>')])
        boldAK = sf.Filter(type='author', contains='A. Kheddar', bold=True)
        bib.toWord(r"[Calibri][{%F% %Last%}{, }{ and }{}]%author%<?, ?>[i][]%title%<?, ?>{[u][]%booktitle%|[u][]%journal%}<?, ?>%year%", [boldAK], out=outPath+'/testStyle')
        
    def testBasicYaml(self):
        bib = Biblio.Biblio.fromBibFile(dataPath + '/sample.bib').resolveCrossref()
        with open(outPath + '/test.yml', 'w', encoding='utf-8') as f:
            for e in bib.entries:
                l = str(e.format(("- id: %ID%\n"
                                  "  year: %year%\n"
                                  "  title: %title%\n"
                                  "  booktitle: {%booktitle%|%journal%}\n"
                                  "  authors:\n[{    - family: %Last%\n      given : %First%}{\n}{}{}]%author%\n"
                                  "<  pdf : ?>%pdf%|%url%<?\n>")))
                f.write(l)
        
            
if __name__ == '__main__':
    unittest.main()