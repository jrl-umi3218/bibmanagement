from bibmanagement.check import Crossref
from bibmanagement.Biblio import Biblio
from .. import testEntries
import unittest

class TestCrossRef(unittest.TestCase):
    def test_unused(self):
        entries = testEntries()
 
        cu = {'ID':'conf:foo:2006',
              'ENTRYTYPE': 'Proceedings',
              'title': 'Foo/Bar conference',
              'year': 2006,
              'address': 'Someplace, somewhere',
              'month' : 'October 9--15',
              'booktitle': 'Foo/Bar conference'
             }
        entries.append(cu)
        
        bib = Biblio(entries)
        
        u = Crossref.unusedProceedings(bib)
        self.assertEqual(len(u), 1)
        self.assertEqual(u[0], 'conf:foo:2006')
        
    def test_duplicate(self):
        entries = testEntries()
        [e1, e2, e3, e4, e5, e6, e7, c1, c2, c3, c4, c5, c6] = entries
        
        # Introducing some fields duplications
        e1['journal'] = 'Acta Laryngol.'
        e4['year'] = 1974
        e4['address'] = 'Châteauneuf-en-Thymerais'
        e4['booktitle'] = 'Institute of advanced typos'
        
        bib = Biblio(entries)
        
        [d,o] = Crossref.duplicatedFields(bib)
        
        self.assertEqual(len(d), 2)
        self.assertEqual(len(o), 2)
        self.assertEqual(d[0][0], 'beulott:ias:1974')
        self.assertEqual(d[0][2], 'year')
        self.assertEqual(d[1][0], 'beulott:ias:1974')
        self.assertEqual(d[1][2], 'address')
        self.assertEqual(o[0][0], 'chou:laryngol:1927')
        self.assertEqual(o[0][2], 'journal')
        self.assertEqual(o[1][0], 'beulott:ias:1974')
        self.assertEqual(o[1][2], 'booktitle')
        
        
        

if __name__ == '__main__':
    unittest.main()