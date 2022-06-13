from bibmanagement.check import Keys
from bibmanagement.fields import Journal
from bibmanagement.fields import Booktitle
from bibmanagement import Biblio
import logging
import logging.handlers
import unittest
import os

class TestKeys(unittest.TestCase):
    def test_clean(self):
        self.assertEqual(Keys.removeAccents('àéïôñç'), 'aeionc')
        self.assertEqual(Keys.removeHyphens('test-case--'), 'testcase')
        self.assertEqual(Keys.removeSpaces('  test  case '), 'testcase')
        self.assertEqual(Keys.cleanAscii('- äçì- - ñéî'), 'acinei')
        
    def test_abbr(self):
        dirpath = os.path.dirname(os.path.abspath(__file__))
        bib = Biblio.Biblio.fromBibFile(dirpath+'/../data/sample.bib')
        Journal.Journal.readVectorList(dirpath+'/../data/sample_journal.json')
        Journal.Journal._vectorList['Another Journal'] = {'name': 'Another Journal'}
        Booktitle.Booktitle.readVectorList(dirpath+'/../data/sample_conf.json')
        Booktitle.Booktitle._vectorList['Another Conference'] = {'name': 'Another Conference'}
        
        self.assertEqual(Keys.getJournalAbbr('Autonomous Robots', None).lower(), 'auro')
        self.assertFalse(Keys.getJournalAbbr('Another Journal', None))
        self.assertEqual(Keys.getJournalAbbr('IEEE International Conference on Robotics and Automation', None).lower(), 'icra')
        self.assertFalse(Keys.getJournalAbbr('Another Conference', None))
    
        e = bib['kanehiro:ar:2014']
        self.assertEqual(Keys.extractProceedingsAbbr(e), 'ar')
        
    def test_generate(self):
        dirpath = os.path.dirname(os.path.abspath(__file__))
        bib = Biblio.Biblio.fromBibFile(dirpath+'/../data/sample.bib')
        Journal.Journal.readVectorList(dirpath+'/../data/sample_journal.json')
        Booktitle.Booktitle.readVectorList(dirpath+'/../data/sample_conf.json')
        
        self.assertEqual(Keys.generatePublicationKey(bib['samadi:ral:2021']), 'samadi:ral:2021')
        self.assertEqual(Keys.generatePublicationKey(bib['yoshida:iros:1999']),  'yoshida:iros:1999')
        self.assertEqual(Keys.generateProceedingsKey(bib['conf:icra:2001']), 'conf:icra:2001')
        self.assertEqual(Keys.generateProceedingsKey(bib['jrnl:ral']), 'jrnl:ral')
        
    def test_check(self):
        logger = logging.getLogger('bibmanagement.check.Keys')
        oldLevel = logger.level
        logger.setLevel(logging.INFO)
        mh = logging.handlers.MemoryHandler(100)
        logger.addHandler(mh)
        
        dirpath = os.path.dirname(os.path.abspath(__file__))
        bib = Biblio.Biblio.fromBibFile(dirpath+'/../data/sample.bib')
        Journal.Journal.readVectorList(dirpath+'/../data/sample_journal.json')
        Booktitle.Booktitle.readVectorList(dirpath+'/../data/sample_conf.json')
        
        bib[2].id = 'ayusawa:jrr:2014'
        
        Keys.checkKeys(bib)
        
        self.assertEqual(len(mh.buffer), 12)
        self.assertEqual(mh.buffer[0].entry.id, 'ayusawa:jrr:2014')
        self.assertEqual(mh.buffer[0].type, 'non_canonical_key')
        self.assertEqual(mh.buffer[1].entry.id, 'imamura:work:2016')
        self.assertEqual(mh.buffer[1].type, 'skipping_key_check')
        self.assertEqual(mh.buffer[3].entry.id, 'conf:humanoids:2016')
        self.assertEqual(mh.buffer[3].type, 'no_abbreviation')
        self.assertEqual(mh.buffer[10].entry.id, 'jrnl:jst')
        self.assertEqual(mh.buffer[10].type, 'failed_to_generate_key')
        
        
        logger.setLevel(oldLevel)
        

if __name__ == '__main__':
    unittest.main()